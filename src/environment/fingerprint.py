"""Record reproducibility metadata without reading credentials or arbitrary environment values."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]

def version(args):
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=30)
    return {"exit_code":p.returncode,"text":(p.stdout+p.stderr).strip()}

def main():
    artifacts=[]
    for path in sorted((ROOT/"work/dependencies").glob("*.jar")):
        artifacts.append({"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    sources=[]
    for directory in (ROOT/"src",ROOT/"tests"):
        for path in sorted(directory.rglob("*")):
            if path.is_file() and path.suffix in {".java",".py",".ps1",".txt"}:
                sources.append({"path":str(path.relative_to(ROOT)),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    result={"captured_utc":datetime.now(timezone.utc).isoformat(),"platform":platform.platform(),
            "python":platform.python_version(),"java":version(["java","-version"]),
            "javac":version(["javac","-version"]),"git":version(["git","--version"]),
            "defects4j_commit":version(["git","-C","work/environments/defects4j","rev-parse","HEAD"]),
            "artifacts":artifacts,"implementation_sources":sources,"no_credentials_recorded":True}
    target=ROOT/"outputs/environment-manifest.json"
    target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(target)

if __name__=="__main__": main()
