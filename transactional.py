"""Authenticated journal-backed inspection; trusted local database required."""
import hashlib
import hmac
from alpha_gateway import validate
from security import sign
from journal import Journal
from workspace import read_artifact
from omega import canonical

def seal(record, key):
    return {"record":record,"tag":hmac.new(key,b"omega-task-v1\0"+canonical(record),hashlib.sha256).hexdigest()}

def inspect(request, signature, key, database, root):
    expected = sign(request,key)
    if not isinstance(signature,str) or not signature.isascii() or not hmac.compare_digest(expected,signature):
        raise ValueError("authentication failed")
    ident, operation = validate(request)
    if operation not in ("synthesize","repair"):
        raise ValueError("unsupported inspection operation")
    journal = Journal(database)
    journal.begin(ident)
    try:
        data = read_artifact(root,ident)
    except (OSError,ValueError,NotImplementedError) as exc:
        record = {"id":ident,"status":"failed","error":type(exc).__name__}
        journal.finish(ident,"failed",seal(record,key))
        raise
    record = {"id":ident,"status":"completed","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
    evidence = seal(record,key)
    journal.finish(ident,"completed",evidence)
    return evidence

def verify_record(ident, status, evidence, key):
    record = evidence["record"]
    if record["id"] != ident or record["status"] != status:
        return False
    return hmac.compare_digest(seal(record,key)["tag"],evidence["tag"])
