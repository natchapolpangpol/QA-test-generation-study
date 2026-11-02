"""Validate four generators on one educational fixture, not on a Defects4J bug."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("aggregate",ROOT/"src/measurement/aggregate.py")
aggregate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(aggregate)

def run(args,log):
    p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=60)
    log.write_text(p.stdout+"\nSTDERR:\n"+p.stderr,encoding="utf-8")
    return p

def main():
    dependencies=[ROOT/"work/dependencies/junit-4.13.2.jar",ROOT/"work/dependencies/hamcrest-core-1.3.jar"]
    instrument_cp=os.pathsep.join(map(str,[ROOT/"work/build/measurement",ROOT/"work/dependencies/javaparser-core-3.26.3.jar"]))
    measurements=ROOT/"work/build/measurement"
    target=ROOT/"tests/golden/AiTarget.java"
    cases=[("codex-sol-smoke-001","GeneratedTest","GeneratedTest.java"),
           ("codex-terra-smoke-001","GeneratedTest","GeneratedTest.java"),
           ("dynamosa-smoke-002","AiTarget_ESTest","tests/AiTarget_ESTest.java"),
           ("mio-smoke-002","AiTarget_ESTest","tests/AiTarget_ESTest.java")]
    results=[]
    for name,test_class,relative in cases:
        path=ROOT/"work/runs"/name
        meta=json.loads((path/"metadata.json").read_text(encoding="utf-8"))
        assert meta["status"]=="generated_not_yet_validated", meta
        test=path/relative
        plain=path/"validation/original"
        replay=path/"validation/instrumented"
        buggy=path/"validation/synthetic-mutant"
        for d in (plain,replay,buggy): d.mkdir(parents=True,exist_ok=True)
        dep_cp=os.pathsep.join(map(str,dependencies))
        p=run(["javac","--release","11","-cp",dep_cp,"-d",plain,target,test],plain/"compile.log")
        assert p.returncode==0,p.stderr
        original_runs=[]
        for repeat in range(3):
            p=run(["java","-cp",os.pathsep.join(map(str,[plain]+dependencies)),"org.junit.runner.JUnitCore",test_class],plain/f"run-{repeat}.log")
            assert p.returncode==0,p.stdout+p.stderr
            original_runs.append(p.returncode)
        p=run(["java","-cp",instrument_cp,"sqa.Instrument",target,replay/target.name,replay/"inventory.json","classify"],replay/"instrument.log")
        assert p.returncode==0,p.stderr
        p=run(["javac","--release","11","-cp",os.pathsep.join(map(str,[measurements]+dependencies)),"-d",replay,replay/target.name,test],replay/"compile.log")
        assert p.returncode==0,p.stderr
        p=run(["java",f"-Dsqa.trace={replay/'trace.tsv'}","-cp",os.pathsep.join(map(str,[replay,measurements]+dependencies)),"org.junit.runner.JUnitCore",test_class],replay/"run.log")
        assert p.returncode==0,p.stdout+p.stderr
        summary=aggregate.summarize(json.loads((replay/"inventory.json").read_text()),[replay/"trace.tsv"])
        (replay/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
        # A deliberately altered teaching example is a plumbing test, not an actual benchmark bug.
        (buggy/target.name).write_text(target.read_text().replace("a > 10 && b > 20","a > 10 || b > 20"),encoding="utf-8")
        p=run(["javac","--release","11","-cp",dep_cp,"-d",buggy,buggy/target.name,test],buggy/"compile.log")
        assert p.returncode==0,p.stderr
        mutants=[]
        for repeat in range(3):
            p=run(["java","-cp",os.pathsep.join(map(str,[buggy]+dependencies)),"org.junit.runner.JUnitCore",test_class],buggy/f"run-{repeat}.log")
            assert p.returncode==1 and "AssertionError" in p.stdout,p.stdout+p.stderr
            mutants.append(p.returncode)
        results.append({"run":name,"generation":meta,"original_passes":len(original_runs),"synthetic_mutant_assertion_failures":len(mutants),"coverage":summary})
        print("PASS",name,flush=True)
    out=ROOT/"outputs/generator-smoke-results.json"
    out.write_text(json.dumps({"status":"passed","scope":"AiTarget.classify teaching fixture only","not_defects4j_results":True,"runs":results},indent=2),encoding="utf-8")
    print("Saved",out)

if __name__=="__main__": main()
