"""Native extraction of the official Defects4J archive on Windows (no deletion)."""
import json
from pathlib import Path
import stat
import shutil
import time
import zipfile
import zlib

ROOT=Path(__file__).resolve().parents[2]
base=(ROOT/"work/environments/defects4j/project_repos").resolve()
archive=base/"defects4j-repos-v3.zip"
start=time.monotonic()
with zipfile.ZipFile(archive) as z:
    for entry in z.infolist():
        resolved=(base/entry.filename).resolve()
        if not resolved.is_relative_to(base): raise RuntimeError("Unsafe archive path")
        if stat.S_ISLNK(entry.external_attr>>16): raise RuntimeError("Symlink not supported by native extractor")
    for entry in z.infolist():
        resolved=(base/entry.filename).resolve()
        if entry.is_dir():
            resolved.mkdir(parents=True,exist_ok=True)
            continue
        resolved.parent.mkdir(parents=True,exist_ok=True)
        if resolved.is_file():
            if resolved.stat().st_size==entry.file_size and zlib.crc32(resolved.read_bytes())==entry.CRC:
                continue
            # These are only prior partial copies of the verified archive in our work directory.
            resolved.chmod(stat.S_IREAD|stat.S_IWRITE)
        with z.open(entry) as source, resolved.open("wb") as target:
            shutil.copyfileobj(source,target,1024*1024)
    count=len(z.infolist())
print(json.dumps({"entries":count,"elapsed_seconds":round(time.monotonic()-start,2),"output":str(base/"defects4j/project_repos")},indent=2))
