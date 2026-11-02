"""Run original/instrumented Java, compare semantics and independently specified counts."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aggregate", ROOT/"src/measurement/aggregate.py")
aggregate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aggregate)
JAVA = os.environ.get("SQA_JAVA", "java")
JAVAC = os.environ.get("SQA_JAVAC", "javac")
JAR = ROOT/"work/dependencies/javaparser-core-3.26.3.jar"
JAR_HASH = "a24c4fa7799ffe0c7a9af11d4eecd757098ed4498f86067bf28b46b2bfea1833"

def command(args, ok=True):
    p = subprocess.run([str(a) for a in args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, timeout=60)
    if ok and p.returncode:
        raise RuntimeError(f"Command failed: {args}\n{p.stdout}\n{p.stderr}")
    return p

def main():
    if hashlib.sha256(JAR.read_bytes()).hexdigest() != JAR_HASH:
        raise RuntimeError("JavaParser artifact hash mismatch")
    build = ROOT/"work/build/measurement"
    build.mkdir(parents=True, exist_ok=True)
    command([JAVAC, "--release", "11", "-cp", JAR, "-d", build, ROOT/"src/measurement/Trace.java", ROOT/"src/measurement/Instrument.java"])
    cp = os.pathsep.join(map(str,[build,JAR]))
    source = ROOT/"tests/golden/TeachingExamples.java"
    runner = ROOT/"tests/golden/GoldenRunner.java"
    base = ROOT/"work/golden/original"
    base.mkdir(parents=True, exist_ok=True)
    command([JAVAC,"--release","11","-d",base,source,runner])
    cases = [
        ("eager", "eager", {"condition":(4,4),"decision":(1,2),"condition_decision":(5,6)}),
        ("shortCircuit", "short", {"condition":(3,4),"decision":(1,2),"condition_decision":(4,6)}),
        ("eager", "eagerFull", {"condition":(4,4),"decision":(2,2),"condition_decision":(6,6)}),
        ("shortCircuit", "shortFull", {"condition":(4,4),"decision":(2,2),"condition_decision":(6,6)}),
        ("countWords", "countOne", {"block":(10,10),"decision":(5,6),"line":(7,7),"statement":(11,11)}),
        ("countWords", "countBoth", {"block":(10,10),"decision":(6,6)}),
        ("countWords", "countRepeat", {"block":(10,10),"decision":(5,6)}),
        ("countWords", "countEmpty", {"block":(5,10),"decision":(2,6)}),
        ("sideEffects", "side", {"condition":(3,4),"decision":(2,2)}),
        ("exceptional", "exception", {"condition":(0,4),"decision":(0,2),"block":(1,3)}),
        ("whileLoop", "while", {"condition":(2,2),"decision":(2,2),"block":(4,4)}),
        ("nestedConditions", "nested", {"condition":(5,6),"decision":(2,2),"condition_decision":(7,8)}),
        ("eagerOr", "or", {"condition":(2,4),"decision":(1,2)}),
        ("booleanXor", "xor", {"condition":(3,4),"decision":(2,2)}),
        ("emptyItems", "noDecisions", {"condition":(0,0),"decision":(0,0),"condition_decision":(0,0)}),
    ]
    results=[]
    for method, name, expected in cases:
        run = ROOT/"work/golden"/name
        run.mkdir(parents=True, exist_ok=True)
        generated = run/source.name
        inventory_file=run/"inventory.json"
        command([JAVA,"-cp",cp,"sqa.Instrument",source,generated,inventory_file,method])
        command([JAVAC,"--release","11","-cp",build,"-d",run,generated,runner])
        original=command([JAVA,"-cp",base,"GoldenRunner",name])
        measured=command([JAVA,f"-Dsqa.trace={run/'trace.tsv'}","-cp",os.pathsep.join(map(str,[run,build])),"GoldenRunner",name])
        if original.stdout != measured.stdout or original.stderr != measured.stderr:
            raise AssertionError(f"Semantic mismatch for {name}")
        inventory=json.loads(inventory_file.read_text(encoding="utf-8"))
        summary=aggregate.summarize(inventory,[run/"trace.tsv"])
        for metric, counts in expected.items():
            actual=summary["metrics"][metric]
            assert (actual["covered"],actual["total"])==counts, (name,metric,actual,counts)
        (run/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
        # Graph uses source-level decisions, so atomic short-circuit jumps are not extra decision edges.
        dot=['digraph coverage {']
        for node in inventory["cfg_nodes"]:
            label=node["id"]+"\\n"+node["type"]
            dot.append(f'  "{node["id"]}" [label="{label}"];')
        for edge in inventory["cfg_edges"]:
            dot.append(f'  "{edge["from"]}" -> "{edge["to"]}" [label="{edge["label"]}"];')
        (run/"cfg.dot").write_text("\n".join(dot+['}']),encoding="utf-8")
        results.append({"case":name,"expected":expected,"result":summary,"semantics_match":True})
        print("PASS",name,flush=True)
    # Unsupported constructs must stop measurement, rather than hide uncovered items.
    for method in ("unsupported","multiline"):
        p=command([JAVA,"-cp",cp,"sqa.Instrument",source,base/"reject.java",base/"reject.json",method],ok=False)
        assert p.returncode != 0, f"Unsupported input was accepted: {method}"
        print("PASS reject",method,flush=True)
    assert results[4]["result"]["metrics"] == results[6]["result"]["metrics"], "Repeats changed coverage"
    assert results[-1]["result"]["metrics"]["decision"]["percent"] is None, "Zero denominator is N/A"
    assert results[-4]["result"]["metrics"]["condition_decision"]["percent"] == 87.5, "C/DC must use counts, not average percentages"
    bad=ROOT/"work/golden/unknown.tsv"
    bad.write_text("1\t1\tcondition\tUNKNOWN:T\n",encoding="utf-8")
    try:
        aggregate.summarize(inventory,[bad])
        raise AssertionError("Unknown trace accepted")
    except ValueError:
        pass
    empty=ROOT/"work/golden/empty.tsv"
    empty.write_text("",encoding="utf-8")
    empty_summary=aggregate.summarize(inventory,[empty])
    assert empty_summary["metrics"]["line"]["covered"]==0
    try:
        aggregate.summarize(inventory,[ROOT/"work/golden/does-not-exist.tsv"])
        raise AssertionError("Missing trace was treated as zero")
    except FileNotFoundError:
        pass
    dest=ROOT/"outputs/golden-validation.json"
    dest.write_text(json.dumps({"status":"passed","java":command([JAVA,"-version"]).stderr.strip(),"cases":results,"unsupported_rejected":["switch","multiline"],"extra_checks":["repeat_union","unknown_trace_rejected","zero_denominator_NA","weighted_CDC","empty_trace_zero","missing_trace_error"]},indent=2),encoding="utf-8")
    print(f"Saved {dest}")

if __name__ == "__main__":
    main()
