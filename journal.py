"""Local transactional journal; database must be trusted."""
import sqlite3
import json
from contextlib import closing
from omega import canonical

class Journal:
    def __init__(self, database):
        self.database = database
        with closing(sqlite3.connect(database)) as c, c:
            c.execute("CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, status TEXT NOT NULL, evidence BLOB)")
    def begin(self, ident):
        with closing(sqlite3.connect(self.database)) as c, c:
            c.execute("INSERT INTO tasks VALUES (?, 'running', NULL)", (ident,))
    def finish(self, ident, status, evidence):
        if status not in ("completed", "failed", "interrupted"):
            raise ValueError("invalid terminal state")
        payload = canonical(evidence)
        with closing(sqlite3.connect(self.database)) as c, c:
            result = c.execute("UPDATE tasks SET status=?, evidence=? WHERE id=? AND status='running'", (status,payload,ident))
            if result.rowcount != 1:
                raise ValueError("task not running")
    def get(self, ident):
        with closing(sqlite3.connect(self.database)) as c:
            row = c.execute("SELECT status,evidence FROM tasks WHERE id=?", (ident,)).fetchone()
        if row is None:
            raise KeyError(ident)
        return row[0], json.loads(row[1]) if row[1] is not None else None
    def pending(self):
        with closing(sqlite3.connect(self.database)) as c:
            return [r[0] for r in c.execute("SELECT id FROM tasks WHERE status='running' ORDER BY id")]
