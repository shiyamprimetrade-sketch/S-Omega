"""Envelope validation only; does not authorize or execute Alpha code."""
import re

def validate(request):
    if not isinstance(request, dict) or type(request.get("version")) is not int or request["version"] != 2:
        raise ValueError("unsupported protocol")
    ident = request.get("id")
    if not isinstance(ident, str) or re.fullmatch(r"[A-Za-z0-9_-]{1,64}", ident) is None:
        raise ValueError("invalid task id")
    op = request.get("operation")
    if op not in ("synthesize", "repair", "knowledge"):
        raise ValueError("unsupported operation")
    if op in ("synthesize", "repair"):
        spec = request.get("spec")
        if not isinstance(spec, dict) or not {"parameters", "expression"} <= spec.keys():
            raise ValueError("missing specification")
    if op == "repair" and "candidate" not in request:
        raise ValueError("missing candidate")
    return ident, op
