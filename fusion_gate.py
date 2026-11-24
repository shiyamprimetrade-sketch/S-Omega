"""Trusted local orchestration gate; not a sandbox."""
import hmac
from alpha_gateway import validate
from security import sign
from journal import Journal
from transactional import seal
from omega import proof

def execute(request, signature, key, database, worker):
    expected=sign(request,key)
    if not isinstance(signature,str) or not signature.isascii() or not hmac.compare_digest(expected,signature):
        raise ValueError("authentication failed")
    ident,operation=validate(request)
    if operation!="synthesize":
        raise ValueError("operation not authorized")
    journal=Journal(database)
    journal.begin(ident)
    try:
        result=worker(request)
        evidence=seal({"id":ident,"status":"completed","request_digest":proof(request),"result":result},key)
        journal.finish(ident,"completed",evidence)
        return evidence
    except Exception as exc:
        journal.finish(ident,"failed",seal({"id":ident,"status":"failed","error":type(exc).__name__},key))
        raise
