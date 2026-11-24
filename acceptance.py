"""Run a disposable end-to-end prototype acceptance check."""
import json
import secrets
import tempfile
from pathlib import Path
from api import inspect, sign, verify_record, Journal, interrupt, anchor_record, check_record

def run():
    results={}
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        db=str(root/"state.db")
        key=secrets.token_bytes(32)
        request={"version":2,"id":"demo","operation":"synthesize","spec":{"parameters":[],"expression":"1"}}
        (root/"demo").mkdir()
        (root/"demo"/"compute.py").write_text("def compute(): return 1\n",encoding="utf-8")
        signature=sign(request,key)
        evidence=inspect(request,signature,key,db,root)
        results["inspection"]=evidence["record"]["bytes"]>0
        results["authentication"]=verify_record("demo","completed",evidence,key)
        results["persistence"]=Journal(db).get("demo")==("completed",evidence)
        anchor=anchor_record(db,"demo",1,key)
        results["anchor"]=check_record(db,"demo",1,key,anchor)
        try:
            inspect(request,"invalid",key,db,root)
        except ValueError:
            results["invalid_signature"]=True
        Journal(db).begin("interrupted")
        results["pending"]=Journal(db).pending()==["interrupted"]
        recovered=interrupt(db,"interrupted",key,exclusive=True)
        results["recovery"]=verify_record("interrupted","interrupted",recovered,key)
        results["terminal_state"]=Journal(db).pending()==[]
    return results

if __name__=="__main__":
    results=run()
    print(json.dumps(results,indent=2,sort_keys=True))
    raise SystemExit(0 if len(results)==8 and all(results.values()) else 1)
