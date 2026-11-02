"""Prepare identical, fixed-only AI context and generation metadata for an exploratory pilot."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]

def main():
    work=ROOT/"work/pilot/Cli-1-v02"; work.mkdir(parents=True,exist_ok=True)
    source_dir=ROOT/"work/checkouts/Cli-1f/src/java/org/apache/commons/cli"
    target=source_dir/"CommandLine.java"
    build=ROOT/"work/build/measurement"
    jar=ROOT/"work/dependencies/javaparser-core-3.26.3.jar"
    subprocess.run(["javac","--release","11","-cp",str(jar),"-d",str(build),str(ROOT/"src/measurement/ApiContext.java")],check=True)
    subprocess.run(["java","-cp",str(build)+":"+str(jar),"sqa.ApiContext",str(source_dir),str(work/"dependency-api.txt")],check=True)
    prompt="""You are a unit-test generator in a controlled experiment. Do not use tools,
inspect files, execute commands, browse the web, or use external project knowledge.
All allowed context is below. Return JSON with java_source containing a complete JUnit
4.13.2 class named GeneratedTest in package org.apache.commons.cli, compatible with
Java 11. Only produce tests; do not reproduce or alter production code.

Create a test suite for the supplied reference class CommandLine. Seek source line,
block, decision and atomic-condition coverage. Use meaningful concrete assertions.
Preserve expected behavior of the reference. You may use package-visible APIs because
the test is in the same package. Use only the supplied version's APIs plus Java/JUnit.
Do not mock the class under test, use reflection, read files, use networking, or spawn
processes. Do not write tests for private methods directly. Tests should be independent
and deterministic. This is the first generation; no execution feedback is available.

REFERENCE CLASS:
"""+target.read_text()+"\nDEPENDENCY API SIGNATURES (not executable source):\n"+(work/"dependency-api.txt").read_text()
    (work/"prompt.txt").write_text(prompt)
    metadata={"phase":"exploratory pilot; not main study","project":"Cli","bug_id":1,
        "target":"org.apache.commons.cli.CommandLine","generation_revision":"fixed",
        "measurement_scope":"17 declared method bodies; constructors/field initializers excluded explicitly",
        "prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),"target_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
        "algorithms":["DYNAMOSA","MIO"],"search_budget_seconds":60,"seeds":[101],
        "models":["gpt-6.1-sol","gpt-6.1-terra"],"model_generations":1,"repairs":0,
        "no_buggy_feedback_to_generators":True,"no_benchmark_tests_in_prompts":True,
        "interpretation":"workflow feasibility only; unequal generation budgets and one repeat do not establish a winner"}
    (work/"protocol.json").write_text(json.dumps(metadata,indent=2))
    print("Prepared pilot context:",len(prompt),"characters")

if __name__=="__main__": main()
