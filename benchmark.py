import json
import time
import statistics
from acceptance import run

def benchmark():
    samples=[]
    for _ in range(20):
        start=time.perf_counter()
        result=run()
        if len(result)!=8 or not all(result.values()):
            raise RuntimeError("acceptance failed")
        samples.append((time.perf_counter()-start)*1000)
    return {"iterations":20,"median_ms":statistics.median(samples),"max_ms":max(samples),"checks_per_iteration":8}

if __name__=="__main__":
    print(json.dumps(benchmark(),indent=2))
