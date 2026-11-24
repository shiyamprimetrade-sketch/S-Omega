"""Trusted local orchestration gate; not an OS sandbox."""
import hmac
from security import sign
from alpha_gateway import validate
from journal import Journal
from transactional import seal
from omega import proof

def execute(request, signature, key, database, runner, *, allowed=()):
    expected=sign(request,key)
    if not isinstance(signature,str) or not signature.isascii() or not hmac.compare_digest(expected,signature):
        raise ValueError("authentication failed")
    ident,operation=validate(request)
    if operation not in ("synthesize","repair") or operation not in allowed:
        raise ValueError("operation denied")
    digest=proof(request)
    journal=Journal(database)
    journal.begin(ident)
    try:
        result=runner(request)
        if proof(request)!=digest:
            raise ValueError("request mutated")
        record={"id":ident,"status":"completed","request_digest":digest,"result_digest":proof(result),"result":result}
    except Exception as exc:
        record={"id":ident,"status":"failed","request_digest":digest,"error":type(exc).__name__}
        journal.finish(ident,"failed",seal(record,key))
        raise
    evidence=seal(record,key)
    journal.finish(ident,"completed",evidence)
    return result,evidence
