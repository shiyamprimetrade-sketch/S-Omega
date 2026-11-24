import hashlib
from security import claim
from continuum import Store
from workspace import read_artifact

def inspect(request, signature, key, database, root):
    ident, operation = claim(request, signature, key, database)
    if operation not in ("synthesize", "repair"):
        raise ValueError("artifact inspection requires synthesis or repair")
    data = read_artifact(root, ident)
    evidence = {"version": 2, "id": ident, "operation": operation,
                "status": "artifact_inspected", "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data)}
    Store(database, key).save(ident, evidence)
    return evidence
