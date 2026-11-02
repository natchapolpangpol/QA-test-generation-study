"""Check one real Defects4J fixed/buggy baseline; benchmark-owned tests are never generated-test coverage."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
D4J=ROOT/"work/environments/defects4j/framework/bin/defects4j"

def execute(args, cwd, log):
    env=dict(os.environ,TZ="America/Los_Angeles",LANG="C.UTF-8")
    started=time.monotonic()
    log.parent.mkdir(parents=True,exist_ok=True)
    stdout_path=log.with_suffix(".stdout")
    with stdout_path.open("w",encoding="utf-8") as out, log.open("w",encoding="utf-8") as err:
        process=subprocess.run([str(x) for x in args],cwd=cwd,env=env,text=True,stdout=out,stderr=err,timeout=1200)
    p=subprocess.CompletedProcess(args,process.returncode,stdout_path.read_text(encoding="utf-8"),log.read_text(encoding="utf-8"))
    log.write_text(p.stdout+"\nSTDERR:\n"+p.stderr,encoding="utf-8")
    return p,{"command":[str(x) for x in args],"exit_code":p.returncode,"elapsed_seconds":round(time.monotonic()-started,3),"log":str(log.relative_to(ROOT))}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--project",default="Cli")
    parser.add_argument("--bug",type=int,default=1)
    a=parser.parse_args()
    logdir=ROOT/"work/baseline"/f"{a.project}-{a.bug}"
    logdir.mkdir(parents=True,exist_ok=True)
    result={"phase":"environment baseline, not generator study","project":a.project,"bug_id":a.bug,
            "started_utc":datetime.now(timezone.utc).isoformat(),"timezone":"America/Los_Angeles","revisions":{},"status":"running"}
    dest=ROOT/"outputs/defects4j-baseline.json"
    def save(): dest.write_text(json.dumps(result,indent=2),encoding="utf-8")
    save()
    try:
        p,meta=execute([D4J,"info","-p",a.project,"-b",a.bug],ROOT,logdir/"info.log")
        result["info"]=meta
        if p.returncode: raise RuntimeError("Defects4J info failed; inspect init status")
        for revision in ("f","b"):
            target=ROOT/"work/checkouts"/f"{a.project}-{a.bug}{revision}"
            data={"path":str(target.relative_to(ROOT)),"steps":[]}
            result["revisions"][revision]=data
            if not target.exists():
                target.parent.mkdir(parents=True,exist_ok=True)
                p,meta=execute([D4J,"checkout","-p",a.project,"-v",f"{a.bug}{revision}","-w",target],ROOT,logdir/f"{revision}-checkout.log")
                data["steps"].append(meta)
                if p.returncode: raise RuntimeError(f"Checkout failed: {revision}")
            # Existing checkouts are reused only if Defects4J identifies the intended version.
            config=(target/".defects4j.config").read_text()
            if f"pid={a.project}" not in config or f"vid={a.bug}{revision}" not in config:
                raise RuntimeError("Checkout identity mismatch")
            for key in ("classes.modified","tests.trigger","dir.src.classes","dir.bin.classes","cp.test"):
                p,meta=execute([D4J,"export","-p",key],target,logdir/f"{revision}-{key}.log")
                data["steps"].append(meta)
                if p.returncode: raise RuntimeError(f"Metadata export failed: {key}")
                data[key]=p.stdout.strip()
            p,meta=execute([D4J,"compile"],target,logdir/f"{revision}-compile.log")
            data["steps"].append(meta)
            if p.returncode: raise RuntimeError(f"Compile failed: {revision}")
            p,meta=execute([D4J,"test"],target,logdir/f"{revision}-test.log")
            data["steps"].append(meta)
            matches=re.findall(r"Failing tests:\s*(\d+)",p.stdout+p.stderr)
            if not matches: raise RuntimeError(f"Missing test result: {revision}")
            data["failing_tests"]=int(matches[-1])
            data["test_process_exit_code"]=p.returncode
            if p.returncode: raise RuntimeError(f"Test command infrastructure failed: {revision}")
            if revision=="f" and data["failing_tests"]!=0: raise RuntimeError("Fixed baseline has failing tests")
            if revision=="b" and data["failing_tests"]==0: raise RuntimeError("Buggy baseline did not reproduce")
            failing_file=target/"failing_tests"
            data["failure_details"]=failing_file.read_text(errors="replace") if failing_file.exists() else ""
            print(f"PASS baseline {a.project}-{a.bug}{revision}: failing tests={data['failing_tests']}",flush=True)
            save()
        result["status"]="passed"
    except Exception as e:
        result["status"]="failed"
        result["error"]=str(e)
        raise
    finally:
        save()

if __name__=="__main__": main()
