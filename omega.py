"""Provisional offline Omega primitives; not a production security boundary."""
import hashlib
import json

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("utf-8")

def proof(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def verify(value, digest):
    return proof(value) == digest

def authorize(action, allowed=()):
    return isinstance(action, str) and action in allowed and action in ("read", "inspect", "verify")

def checkpoint(state, previous=None):
    record = {"version": 1, "state": json.loads(canonical(state)), "previous": previous}
    return {"record": record, "digest": proof(record)}

def restore(entry):
    if not verify(entry["record"], entry["digest"]):
        raise ValueError("checkpoint integrity failure")
    if entry["record"]["version"] != 1:
        raise ValueError("unsupported version")
    return entry["record"]["state"]
