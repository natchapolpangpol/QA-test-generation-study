"""Audit declared-method instrumentation against the existing Defects4J test suite.

Overlay class files take precedence on the classpath. Neither fixed/buggy checkout
is changed. This validates measurement, not generator performance.
"""
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

def execute(args,log,ok=True):
    p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=180,
                     env=dict(os.environ,TZ="America/Los_Angeles",LANG="C.UTF-8"))
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(p.stdout+"\nSTDERR:\n"+p.stderr)
    if ok and p.returncode: raise RuntimeError(p.stdout+p.stderr)
    return p

def main():
    baseline=json.loads((ROOT/"outputs/defects4j-baseline.json").read_text())
    details=baseline["revisions"]["f"]
    checkout=ROOT/details["path"]
    source=checkout/details["dir.src.classes"]/"org/apache/commons/cli/CommandLine.java"
    original_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    work=ROOT/"work/class-replay/Cli-1f-v02"; work.mkdir(parents=True,exist_ok=True)
    build=ROOT/"work/build/measurement"
    jar=ROOT/"work/dependencies/javaparser-core-3.26.3.jar"
    cp=os.pathsep.join(map(str,[build,jar]))
    execute(["java","-cp",cp,"sqa.Instrument",source,work/"CommandLine.java",work/"inventory.json","class:CommandLine"],work/"instrument.log")
    junit=ROOT/"work/dependencies/junit-4.13.2.jar"
    hamcrest=ROOT/"work/dependencies/hamcrest-core-1.3.jar"
    # The fresh JUnit 4 runner can execute the existing JUnit 3 tests. Remove the older JUnit jar.
    paths=[p for p in details["cp.test"].split(os.pathsep) if "junit-3.8.1.jar" not in p]
    original_cp=os.pathsep.join(map(str,[junit,hamcrest]+paths))
    execute(["javac","--release","11","-cp",os.pathsep.join([str(build),original_cp]),"-d",work,work/"CommandLine.java"],work/"compile.log")
    names=sorted(set(re.findall(r"\(([^()]+)\)", (checkout/"all_tests").read_text())))
    if not names: raise RuntimeError("No benchmark test classes discovered")
    a=execute(["java","-cp",original_cp,"org.junit.runner.JUnitCore",*names],work/"original.log")
    b=execute(["java",f"-Dsqa.trace={work/'trace.tsv'}","-cp",os.pathsep.join([str(work),str(build),original_cp]),"org.junit.runner.JUnitCore",*names],work/"instrumented.log")
    pattern=r"OK \((\d+) tests?\)"
    counts=[re.search(pattern,x.stdout) for x in (a,b)]
    if not all(counts) or counts[0].group(1)!=counts[1].group(1): raise RuntimeError("Original/replay test outcomes differ")
    if hashlib.sha256(source.read_bytes()).hexdigest()!=original_hash: raise RuntimeError("Original source was modified")
    inventory=json.loads((work/"inventory.json").read_text())
    summary=aggregate.summarize(inventory,[work/"trace.tsv"])
    if len(inventory["methods"])!=17: raise RuntimeError("Unexpected selected method inventory")
    # Independent source audit: 8 decisions and 8 atomic conditions in CommandLine.
    if summary["metrics"]["decision"]["total"]!=16 or summary["metrics"]["condition"]["total"]!=16:
        raise RuntimeError("Decision/condition denominator differs from manual source count")
    for kind,total in {"line":38,"statement":42,"block":40}.items():
        if summary["metrics"][kind]["total"]!=total: raise RuntimeError(f"Manual {kind} denominator mismatch")
    result={"status":"passed","phase":"measurement validation using benchmark-owned tests, not generated tests",
        "project":"Cli","bug":1,"revision":"fixed","source_sha256":original_hash,
        "scope_policy":inventory["scope_policy"],"method_count":len(inventory["methods"]),
        "excluded_members":inventory["excluded_members"],"junit_test_count":int(counts[0].group(1)),
        "test_classes":names,"original_passed":True,"instrumented_passed":True,
        "coverage":summary,"work_directory":str(work.relative_to(ROOT))}
    (ROOT/"outputs/class-replay-validation.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({"status":"passed","tests":result["junit_test_count"],"methods":result["method_count"],
        "decision":summary["metrics"]["decision"],"condition":summary["metrics"]["condition"]},indent=2))

if __name__=="__main__": main()
