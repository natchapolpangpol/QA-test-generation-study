"""Run a pinned EvoSuite build and preserve command/log/provenance per attempt."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]

def generate(algorithm, target, project_cp, output, budget=10, seed=101, phase="infrastructure smoke; not main study"):
    output=Path(output).resolve()
    output.mkdir(parents=True,exist_ok=False)
    jar=ROOT/"work/dependencies/evosuite-1.2.0.jar"
    classpath=os.pathsep.join(str(Path(p).resolve()) for p in project_cp.split(os.pathsep))
    args=["java","-jar",str(jar),"-generateMOSuite","-class",target,"-projectCP",classpath,
          "-criterion","BRANCH",f"-Dalgorithm={algorithm}",f"-Dsearch_budget={budget}","-seed",str(seed),
          "-Dassertion_strategy=ALL","-Dno_runtime_dependency=true","-Dreplace_calls=false",
          "-Dvirtual_fs=false","-Dvirtual_net=false","-Dreset_static_fields=false",
          f"-Dtest_dir={output/'tests'}",f"-Dreport_dir={output/'report'}"]
    metadata={"algorithm":algorithm,"target":target,"seed":seed,"search_budget_seconds":budget,
              "phase":phase,"command":args,"timezone":"America/Los_Angeles",
              "started_utc":datetime.now(timezone.utc).isoformat(),
              "evosuite_sha256":hashlib.sha256(jar.read_bytes()).hexdigest(),
              "runtime_policy":"no EvoSuite runtime in emitted tests; pilot policy, not frozen for main study"}
    start=time.monotonic()
    try:
        with (output/"generation.log").open("w",encoding="utf-8") as log:
            p=subprocess.run(args,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,timeout=budget+180,env=dict(os.environ,TZ="America/Los_Angeles"))
        text=(output/"generation.log").read_text(encoding="utf-8")
        selected=f"Total number of test goals for {algorithm}:" in text
        tests=list((output/"tests").rglob("*_ESTest.java"))
        metadata.update(exit_code=p.returncode,algorithm_confirmed_by_log=selected,
                        status="generated_not_yet_validated" if p.returncode==0 and selected and tests else "generation_failed")
    except subprocess.TimeoutExpired:
        metadata["status"]="timeout"
    finally:
        metadata["elapsed_seconds"]=round(time.monotonic()-start,3)
        (output/"metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    return metadata

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--algorithm",choices=["DYNAMOSA","MIO"],required=True)
    p.add_argument("--target",required=True)
    p.add_argument("--project-cp",required=True)
    p.add_argument("--output",required=True)
    p.add_argument("--budget",type=int,default=10)
    p.add_argument("--seed",type=int,default=101)
    p.add_argument("--phase",default="infrastructure smoke; not main study")
    a=p.parse_args()
    result=generate(a.algorithm,a.target,a.project_cp,a.output,a.budget,a.seed,a.phase)
    print(json.dumps({k:result[k] for k in ("algorithm","status","elapsed_seconds")},indent=2))
    raise SystemExit(0 if result["status"]=="generated_not_yet_validated" else 1)
