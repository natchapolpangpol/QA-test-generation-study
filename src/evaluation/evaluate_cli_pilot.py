"""Evaluate frozen, first-generation suites without editing or repairing their tests."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("aggregate",ROOT/"src/measurement/aggregate.py")
aggregate=importlib.util.module_from_spec(spec); spec.loader.exec_module(aggregate)

def execute(args,log):
    log.parent.mkdir(parents=True,exist_ok=True)
    try:
        p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=180,
                         env=dict(os.environ,TZ="America/Los_Angeles",LANG="C.UTF-8"))
        log.write_text(p.stdout+"\nSTDERR:\n"+p.stderr)
        return p
    except subprocess.TimeoutExpired as e:
        log.write_text("PROCESS TIMEOUT\n")
        return subprocess.CompletedProcess(args,124,"","PROCESS TIMEOUT")

def junit_result(p):
    passed=re.search(r"OK \((\d+) tests?\)",p.stdout)
    failed=re.search(r"Tests run: (\d+),\s+Failures: (\d+)",p.stdout)
    if passed and p.returncode==0:
        return {"status":"passed","test_count":int(passed.group(1)),"failure_count":0,"failures":[]}
    if failed and p.returncode==1:
        headers=re.findall(r"(?m)^\d+\) ([^\n]+)",p.stdout)
        return {"status":"test_failures","test_count":int(failed.group(1)),"failure_count":int(failed.group(2)),"failures":headers}
    return {"status":"execution_error","exit_code":p.returncode}

def main():
    baseline=json.loads((ROOT/"outputs/defects4j-baseline.json").read_text())
    measurement=json.loads((ROOT/"outputs/class-replay-validation.json").read_text())
    if baseline["status"]!="passed" or measurement["status"]!="passed": raise RuntimeError("Pilot gates not passed")
    fixed=baseline["revisions"]["f"]; buggy=baseline["revisions"]["b"]
    junit=ROOT/"work/dependencies/junit-4.13.2.jar"; hamcrest=ROOT/"work/dependencies/hamcrest-core-1.3.jar"
    def cp(details):
        items=[p for p in details["cp.test"].split(os.pathsep) if "junit-3.8.1.jar" not in p and "/target/test-classes" not in p]
        return os.pathsep.join(map(str,[junit,hamcrest]+items))
    fixed_cp,buggy_cp=cp(fixed),cp(buggy)
    replay=ROOT/"work/class-replay/Cli-1f-v02"; runtime=ROOT/"work/build/measurement"
    inventory=json.loads((replay/"inventory.json").read_text())
    source=ROOT/fixed["path"]/fixed["dir.src.classes"]/"org/apache/commons/cli/CommandLine.java"
    if hashlib.sha256(source.read_bytes()).hexdigest()!=inventory["source_sha256"]: raise RuntimeError("Scope source changed")
    cases=[("cli1-dynamosa-001","org.apache.commons.cli.CommandLine_ESTest"),
           ("cli1-mio-001","org.apache.commons.cli.CommandLine_ESTest"),
           ("cli1-sol-001","org.apache.commons.cli.GeneratedTest"),
           ("cli1-terra-001","org.apache.commons.cli.GeneratedTest")]
    result={"status":"completed","phase":"exploratory pilot, one generation per method; not main study",
            "project":"Cli","bug_id":1,"revision_for_coverage":"fixed","measurement_version":inventory["measurement_version"],
            "scope":inventory["scope_policy"],"source_sha256":inventory["source_sha256"],"method_count":len(inventory["methods"]),
            "existing_tests_included":False,"repair_responses":0,"suite_policy":"whole suite must pass fixed three times; no manual test removal",
            "runs":[]}
    for name,test_class in cases:
        folder=ROOT/"work/runs"/name
        metadata=json.loads((folder/"metadata.json").read_text())
        record={"run":name,"generator":metadata,"status":"pending"}
        result["runs"].append(record)
        if metadata["status"]!="generated_not_yet_validated":
            record["status"]="generation_failed"; continue
        files=sorted((folder/"tests").rglob("*.java")) if (folder/"tests").is_dir() else [folder/"GeneratedTest.java"]
        record["suite_files"]=[{"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
        validation=folder/"validation-v02"; classes=validation/"classes"; classes.mkdir(parents=True,exist_ok=True)
        p=execute(["javac","--release","11","-cp",fixed_cp,"-d",classes,*files],validation/"compile.log")
        if p.returncode:
            record["status"]="compile_failed"; print(name,record["status"],flush=True); continue
        fixed_runs=[]
        for repeat in range(3):
            p=execute(["java","-cp",str(classes)+os.pathsep+fixed_cp,"org.junit.runner.JUnitCore",test_class],validation/f"fixed-{repeat}.log")
            fixed_runs.append(junit_result(p))
        record["fixed_runs"]=fixed_runs
        if not all(r["status"]=="passed" for r in fixed_runs):
            record["status"]="fixed_validation_failed"; print(name,record["status"],flush=True); continue
        trace=validation/"trace.tsv"
        # The harness creates an empty replay log before execution. If no scoped code runs,
        # it remains empty; a missing log after execution is still an infrastructure error.
        trace.write_text("")
        p=execute(["java",f"-Dsqa.trace={trace}","-cp",os.pathsep.join([str(classes),str(replay),str(runtime),fixed_cp]),"org.junit.runner.JUnitCore",test_class],validation/"coverage.log")
        replay_result=junit_result(p); record["replay"]=replay_result
        if replay_result["status"]!="passed" or replay_result["test_count"]!=fixed_runs[0]["test_count"]:
            record["status"]="measurement_replay_failed"; continue
        if not trace.exists(): raise RuntimeError("Replay log disappeared")
        if trace.stat().st_size==0: record["no_in_scope_execution"]=True
        record["coverage"]=aggregate.summarize(inventory,[trace])
        buggy_runs=[]
        for repeat in range(3):
            p=execute(["java","-cp",str(classes)+os.pathsep+buggy_cp,"org.junit.runner.JUnitCore",test_class],validation/f"buggy-{repeat}.log")
            buggy_runs.append(junit_result(p))
        record["buggy_runs"]=buggy_runs
        stable=all(r["status"]=="test_failures" for r in buggy_runs) and len({tuple(r["failures"]) for r in buggy_runs})==1
        record["reproducible_buggy_failures"]=stable
        record["detection_status"]="candidate_requires_cause_review" if stable else "not_detected_or_inconclusive"
        record["status"]="evaluated"
        print(name,"evaluated; reproducible buggy failures:",stable,flush=True)
    destination=ROOT/"outputs/cli1-pilot-results.json"
    destination.write_text(json.dumps(result,indent=2))
    print("Saved",destination)

if __name__=="__main__": main()
