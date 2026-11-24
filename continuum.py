from contextlib import closing
import hashlib
import hmac
import json
import sqlite3
from omega import canonical

class Store:
    def __init__(self, database, key):
        if not isinstance(key, bytes) or len(key) < 32:
            raise ValueError("key must contain at least 32 bytes")
        self.database, self.key = database, key
        with closing(sqlite3.connect(database)) as conn, conn:
            conn.execute("CREATE TABLE IF NOT EXISTS snapshots (id TEXT PRIMARY KEY, payload BLOB NOT NULL, tag TEXT NOT NULL)")
    def tag(self, ident, payload):
        return hmac.new(self.key, b"omega-checkpoint-v1\0" + canonical([ident, payload.hex()]), hashlib.sha256).hexdigest()
    def save(self, ident, state):
        payload = canonical(state)
        with closing(sqlite3.connect(self.database)) as conn, conn:
            conn.execute("INSERT INTO snapshots VALUES (?, ?, ?)", (ident, payload, self.tag(ident, payload)))
    def load(self, ident):
        with closing(sqlite3.connect(self.database)) as conn, conn:
            row = conn.execute("SELECT payload, tag FROM snapshots WHERE id = ?", (ident,)).fetchone()
        if row is None:
            raise KeyError(ident)
        payload, tag = row
        if not hmac.compare_digest(self.tag(ident, payload), tag):
            raise ValueError("checkpoint authentication failed")
        return json.loads(payload)
