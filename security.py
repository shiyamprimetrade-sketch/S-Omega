from contextlib import closing
import hashlib
import hmac
import sqlite3
from omega import canonical
from alpha_gateway import validate

def sign(request, key):
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError("key must contain at least 32 bytes")
    return hmac.new(key, b"omega-request-v1\0" + canonical(request), hashlib.sha256).hexdigest()

def claim(request, signature, key, database):
    expected = sign(request, key)
    if not isinstance(signature, str) or not signature.isascii() or not hmac.compare_digest(expected, signature):
        raise ValueError("authentication failed")
    ident, operation = validate(request)
    with closing(sqlite3.connect(database)) as conn, conn:
        conn.execute("CREATE TABLE IF NOT EXISTS claims (id TEXT PRIMARY KEY)")
        try:
            conn.execute("INSERT INTO claims VALUES (?)", (ident,))
        except sqlite3.IntegrityError as exc:
            raise ValueError("replayed task") from exc
    return ident, operation
