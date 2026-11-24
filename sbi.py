"""Candidate SBI-001 envelope, not ratified SCC conformance."""
import json
import re
from alpha_gateway import validate

FIELDS={"schema_version","operation_id","capability","deadline_ms","payload"}

def unique(pairs):
    result={}
    for k,v in pairs:
        if k in result:
            raise ValueError("duplicate field")
        result[k]=v
    return result

def reject_constant(value):
    raise ValueError("nonfinite number")

def parse(raw):
    if not isinstance(raw,bytes) or len(raw)>65536:
        raise ValueError("invalid request size")
    try:
        obj=json.loads(raw.decode("utf-8"),object_pairs_hook=unique,parse_constant=reject_constant)
    except (UnicodeError,RecursionError) as exc:
        raise ValueError("invalid request") from exc
    if not isinstance(obj,dict) or set(obj)!=FIELDS or obj["schema_version"]!="1.0":
        raise ValueError("invalid envelope")
    for field,pattern in (("operation_id",r"[A-Za-z0-9_-]{1,128}"),("capability",r"[a-z][a-z0-9_.]{0,127}")):
        if not isinstance(obj[field],str) or not re.fullmatch(pattern,obj[field]):
            raise ValueError("invalid identifier")
    if type(obj["deadline_ms"]) is not int or not 1<=obj["deadline_ms"]<=300000 or not isinstance(obj["payload"],dict):
        raise ValueError("invalid deadline or payload")
    return obj

def translate(obj):
    op={"workspace.synthesize":"synthesize","workspace.repair":"repair"}.get(obj["capability"])
    if op is None:
        raise ValueError("unsupported capability")
    payload=obj["payload"]
    permitted={"spec","expected_cases"} | ({"candidate","max_attempts"} if op=="repair" else set())
    if set(payload)-permitted:
        raise ValueError("unsupported payload field")
    task={**payload,"version":2,"id":obj["operation_id"],"operation":op}
    validate(task)
    return task
