"""Authenticated snapshot receipts; caller must retain trusted anchor externally."""
import hashlib
import hmac
from omega import canonical

def receipt(sequence, state, key):
    if type(sequence) is not int or sequence < 0:
        raise ValueError("invalid sequence")
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("invalid key")
    digest = hashlib.sha256(canonical(state)).hexdigest()
    tag = hmac.new(key, b"omega-receipt-v1\0" + canonical([sequence, digest]), hashlib.sha256).hexdigest()
    return {"sequence": sequence, "digest": digest, "tag": tag}

def verify_anchor(sequence, state, key, anchor):
    expected = receipt(sequence, state, key)
    if not isinstance(anchor, dict) or anchor != expected:
        raise ValueError("checkpoint differs from trusted anchor")
    return True
