"""v0.2 validation: overload selection, type-preserving return ternary, class-method inventory."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("aggregate",ROOT/"src/measurement/aggregate.py")
aggregate=importlib.util.module_from_spec(spec); spec.loader.exec_module(aggregate)

def run(args,ok=True):
    p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=60)
    if ok and p.returncode: raise RuntimeError(p.stdout+p.stderr)
    return p

def main():
    build=ROOT/"work/build/measurement"
    jar=ROOT/"work/dependencies/javaparser-core-3.26.3.jar"
    run(["javac","--release","11","-cp",jar,"-d",build,*sorted((ROOT/"src/measurement").glob("*.java"))])
    toolcp=os.pathsep.join(map(str,[build,jar]))
    original=ROOT/"work/flow/original"; original.mkdir(parents=True,exist_ok=True)
    source=ROOT/"tests/golden/FlowExamples.java"; runner=ROOT/"tests/golden/FlowRunner.java"
    run(["javac","--release","11","-d",original,source,runner])
    cases=[
        ("select(int)","intOverload",{"decision":(2,2),"condition":(2,2),"block":(3,3)}),
        ("FlowExamples#select(String)","stringOverload",{"decision":(2,2),"condition":(4,4)}),
        ("ternary(boolean,boolean)","ternaryFalse",{"decision":(1,2),"condition":(1,4),"block":(2,3),"statement":(2,2),"condition_decision":(2,6)}),
        ("ternary", "ternaryAll",{"decision":(2,2),"condition":(4,4),"block":(3,3)}),
        ("promoted", "promoted",{"decision":(2,2),"condition":(2,2),"block":(3,3)}),
        ("unbox", "unbox",{"decision":(2,2),"condition":(2,2),"block":(3,3)}),
        ("reference", "reference",{"decision":(2,2),"condition":(2,2),"block":(3,3)}),
        ("throwingArm", "throwingArm",{"decision":(2,2),"condition":(2,2),"block":(3,3)}),
        ("conditionThrows", "conditionThrows",{"decision":(0,2),"condition":(0,2),"block":(1,3)}),
        ("class:FlowExamples", "classSubset",{}),
    ]
    results=[]
    for selector,name,expected in cases:
        output=ROOT/"work/flow"/name; output.mkdir(parents=True,exist_ok=True)
        run(["java","-cp",toolcp,"sqa.Instrument",source,output/source.name,output/"inventory.json",selector])
        run(["javac","--release","11","-cp",build,"-d",output,output/source.name,runner])
        a=run(["java","-cp",original,"FlowRunner",name])
        b=run(["java",f"-Dsqa.trace={output/'trace.tsv'}","-cp",os.pathsep.join(map(str,[output,build])),"FlowRunner",name])
        assert (a.stdout,a.stderr)==(b.stdout,b.stderr),(name,a.stdout,b.stdout)
        inventory=json.loads((output/"inventory.json").read_text())
        summary=aggregate.summarize(inventory,[output/"trace.tsv"])
        for kind,pair in expected.items():
            metric=summary["metrics"][kind]
            assert (metric["covered"],metric["total"])==pair,(name,kind,metric,pair)
        # Validate every graph endpoint and two T/F edges for every decision block.
        nodes={n["id"]:n for n in inventory["cfg_nodes"]}
        for edge in inventory["cfg_edges"]:
            assert edge["from"] in nodes and edge["to"] in nodes
        for key,node in nodes.items():
            if node["type"] in {"decision","ternary-decision"}:
                assert sorted(e["label"] for e in inventory["cfg_edges"] if e["from"]==key)==["F","T"]
        if selector.startswith("class:"):
            assert len(inventory["methods"])==12
            assert inventory["excluded_members"][0]["kind"]=="FieldDeclaration"
            untouched=[i["id"] for i in inventory["items"] if "#neverCalled(" in i["id"] and i["kind"]=="decision"]
            assert len(untouched)==2 and set(untouched)<=set(summary["metrics"]["decision"]["uncovered_ids"])
            assert summary["metrics"]["decision"]["total"]==18
            assert summary["metrics"]["condition"]["total"]==22
            assert len(set(i["id"] for i in inventory["items"]))==len(inventory["items"])
        (output/"summary.json").write_text(json.dumps(summary,indent=2))
        results.append({"case":name,"selector":selector,"expected":expected,"summary":summary,"semantics_match":True})
        print("PASS",name,flush=True)
    rejections=[]
    rejected_source=ROOT/"tests/golden/RejectedTernary.java"
    for src,selector in [(source,"select"),(source,"select(double)"),(rejected_source,"nested"),(rejected_source,"initializer"),(rejected_source,"argument"),(rejected_source,"class:RejectedTernary")]:
        output=ROOT/"work/flow/rejected"; output.mkdir(exist_ok=True)
        # Rejected outputs get distinct names; no success artifact may be created.
        index=len(rejections)
        code=output/f"rejected-{index}.java"; manifest=output/f"rejected-{index}.json"
        p=run(["java","-cp",toolcp,"sqa.Instrument",src,code,manifest,selector],ok=False)
        assert p.returncode!=0 and not code.exists() and not manifest.exists(),selector
        rejections.append({"selector":selector,"rejected":True})
    (ROOT/"outputs/flow-validation.json").write_text(json.dumps({"status":"passed","measurement_version":"0.2-prototype","cases":results,"rejections":rejections},indent=2))
    print("Saved flow-validation.json")

if __name__=="__main__": main()
