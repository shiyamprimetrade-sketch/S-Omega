"""Local Fusion arithmetic orchestration; trusted Alpha checkout required."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from fusion_gate import execute
from semantic import verify_source
from workspace import read_artifact

def orchestrate(request, signature, key, database, alpha, *, allowed=()):
    alpha=Path(alpha).resolve()
    def runner(task):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            taskfile=root/"request.json"
            taskfile.write_text(json.dumps(task),encoding="utf-8")
            workspace=root/"workspace"
            proc=subprocess.run([sys.executable,"-m","s_alpha","--db",str(root/"alpha.db"),"execute",str(taskfile),"--out",str(workspace)],cwd=alpha,capture_output=True,text=True,timeout=60,check=True)
            response=json.loads(proc.stdout)
            if response.get("version")!=2 or response.get("id")!=task["id"] or response.get("status")!="verified":
                raise ValueError("Alpha did not verify task")
            source=read_artifact(workspace,task["id"],16384)
            digest=hashlib.sha256(source).hexdigest()
            if response.get("artifact",{}).get("sha256")!=digest or not verify_source(task["spec"],source):
                raise ValueError("independent artifact verification failed")
            return {"alpha":response,"independent_verified":True,"sha256":digest,"source":source.decode("utf-8")}
    return execute(request,signature,key,database,runner,allowed=allowed)
