"""Run trusted local Alpha checkout, then authenticate and inspect its artifact."""
import json
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path
from api import inspect, sign, verify_record, Journal

def run(alpha):
    alpha=Path(alpha).resolve()
    request=json.loads((alpha/"examples/synthesis.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        workspace=root/"workspace"
        result=subprocess.run([sys.executable,"-m","s_alpha","--db",str(root/"alpha.db"),"execute",str(alpha/"examples/synthesis.json"),"--out",str(workspace)],cwd=alpha,capture_output=True,text=True,timeout=60,check=True)
        response=json.loads(result.stdout)
        if response.get("id")!=request["id"] or response.get("version")!=2 or response.get("status")=="failed":
            raise ValueError("unexpected Alpha response")
        key=secrets.token_bytes(32)
        db=str(root/"omega.db")
        evidence=inspect(request,sign(request,key),key,db,workspace)
        ident=request["id"]
        return {"alpha_response":response,"omega_evidence":evidence,"authenticated":verify_record(ident,"completed",evidence,key),"persisted":Journal(db).get(ident)==("completed",evidence)}

if __name__=="__main__":
    result=run(sys.argv[1])
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["authenticated"] and result["persisted"] else 1)
