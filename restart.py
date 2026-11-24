"""Recovery requires exclusive offline ownership of the journal."""
from journal import Journal
from transactional import seal, verify_record
from recovery import receipt, verify_anchor

def interrupt(database, ident, key, *, exclusive=False):
    if exclusive is not True:
        raise ValueError("exclusive offline ownership required")
    if not isinstance(key, bytes) or len(key)<32:
        raise ValueError("invalid key")
    evidence=seal({"id":ident,"status":"interrupted","reason":"offline recovery"},key)
    Journal(database).finish(ident,"interrupted",evidence)
    return evidence

def anchor_record(database, ident, sequence, key):
    status,evidence=Journal(database).get(ident)
    if not verify_record(ident,status,evidence,key):
        raise ValueError("invalid terminal evidence")
    return receipt(sequence,evidence,key)

def check_record(database, ident, sequence, key, anchor):
    status,evidence=Journal(database).get(ident)
    if not verify_record(ident,status,evidence,key):
        raise ValueError("invalid terminal evidence")
    return verify_anchor(sequence,evidence,key,anchor)
