"""Subscription-authenticated Codex CLI adapter for controlled text-only test generation.

This is a benchmark model invocation, not an implementation assistant. Reject any
tool use before admitting generated tests. Does not read or export authentication tokens.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]

def codex_command():
    if os.name == "nt":
        # The installed npm launcher uses this entrypoint. Invoke Node without a shell.
        launcher = shutil.which("codex.cmd") or shutil.which("codex")
        if not launcher:
            raise RuntimeError("Codex CLI not installed")
        entry = Path(launcher).parent/"node_modules/@openai/codex/bin/codex.js"
        if not entry.is_file():
            raise RuntimeError("Unsupported Codex installation; configure a direct executable")
        return [shutil.which("node"),str(entry)]
    return [shutil.which("codex") or "codex"]

def generate(model, prompt_file, output_dir, phase="infrastructure smoke test; not main study"):
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=False)  # Never overwrite an experiment.
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    (output_dir/"prompt.txt").write_text(prompt,encoding="utf-8")
    empty = output_dir/"context"
    empty.mkdir()
    schema = {"type":"object","properties":{"java_source":{"type":"string"}},"required":["java_source"],"additionalProperties":False}
    schema_path = output_dir/"response-schema.json"
    schema_path.write_text(json.dumps(schema),encoding="utf-8")
    executable = codex_command()
    args = executable + ["exec","--ignore-user-config","--skip-git-repo-check","--ephemeral",
        "--sandbox","read-only","--model",model,"-c","model_reasoning_effort=\"low\"",
        "-c","web_search=\"disabled\"","--cd",str(empty),"--output-schema",str(schema_path),
        "--output-last-message",str(output_dir/"response.json"),"--json","-"]
    metadata = {"model_requested":model,"surface":"Codex CLI with ChatGPT subscription",
        "phase":phase,"reasoning_effort":"low",
        "started_utc":datetime.now(timezone.utc).isoformat(),
        "prompt_sha256":hashlib.sha256(prompt.encode()).hexdigest(),"command":args,
        "cli_version":subprocess.run(executable+["--version"],capture_output=True,text=True,timeout=20).stdout.strip()}
    start=time.monotonic()
    try:
        with (output_dir/"events.jsonl").open("w",encoding="utf-8") as stdout, (output_dir/"stderr.log").open("w",encoding="utf-8") as stderr:
            p=subprocess.run(args,input=prompt,text=True,encoding="utf-8",stdout=stdout,stderr=stderr,timeout=300)
        metadata["exit_code"]=p.returncode
        events=[]
        for row in (output_dir/"events.jsonl").read_text(encoding="utf-8").splitlines():
            if row.strip(): events.append(json.loads(row))
        item_types=sorted({e.get("item",{}).get("type") for e in events if e.get("item",{}).get("type")})
        # Unknown event item types are not assumed to be harmless.
        tool_types=[x for x in item_types if x not in {"reasoning","agent_message"}]
        metadata.update(item_types=item_types,tool_events=tool_types,
                        usage=[e.get("usage") for e in events if e.get("usage")])
        if p.returncode:
            metadata["status"]="generation_failed"
        elif tool_types:
            metadata["status"]="rejected_tool_use"
        else:
            response=json.loads((output_dir/"response.json").read_text(encoding="utf-8"))
            code=response["java_source"]
            (output_dir/"GeneratedTest.java").write_text(code,encoding="utf-8")
            metadata.update(status="generated_not_yet_validated",suite_sha256=hashlib.sha256(code.encode()).hexdigest())
    except subprocess.TimeoutExpired:
        metadata["status"]="timeout"
    finally:
        metadata["elapsed_seconds"]=round(time.monotonic()-start,3)
        (output_dir/"metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    return metadata

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--model",required=True)
    p.add_argument("--prompt",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--phase",default="infrastructure smoke test; not main study")
    a=p.parse_args()
    result=generate(a.model,a.prompt,a.output,a.phase)
    print(json.dumps({k:result[k] for k in ("status","model_requested","elapsed_seconds")},indent=2))
    raise SystemExit(0 if result["status"]=="generated_not_yet_validated" else 1)
