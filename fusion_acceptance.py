import json
import secrets
import sys
import tempfile
from pathlib import Path
from fusion import orchestrate
from security import sign
from transactional import verify_record
from journal import Journal

def main(alpha):
    alpha=Path(alpha).resolve()
    request=json.loads((alpha/"examples/synthesis.json").read_text(encoding="utf-8"))
    key=secrets.token_bytes(32)
    with tempfile.TemporaryDirectory() as tmp:
        db=str(Path(tmp)/"fusion.db")
        result,evidence=orchestrate(request,sign(request,key),key,db,alpha,allowed=("synthesize",))
        if not result["independent_verified"] or not verify_record(request["id"],"completed",evidence,key) or Journal(db).get(request["id"])!=("completed",evidence):
            raise RuntimeError("Fusion acceptance failed")
        print(json.dumps({"independent_verified":True,"authenticated":True,"persisted":True,"sha256":result["sha256"]},indent=2))

if __name__=="__main__":
    main(sys.argv[1])
