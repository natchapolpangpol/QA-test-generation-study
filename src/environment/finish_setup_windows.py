"""Finish the already-downloaded official init.sh Gradle/analyzer steps natively on Windows."""
from pathlib import Path
import shutil
import stat
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[2]
D4J=(ROOT/"work/environments/defects4j").resolve()
gradle=D4J/"framework/lib/build_systems/gradle"
for archive,destination in [(gradle/"defects4j-gradle-dists-v3.zip",gradle/"dists"),(gradle/"defects4j-gradle-deps-v3.zip",gradle)]:
    destination.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            target=(destination/info.filename).resolve()
            if not target.is_relative_to(destination.resolve()): raise RuntimeError("Unsafe archive path")
            if stat.S_ISLNK(info.external_attr>>16): raise RuntimeError("Unexpected symbolic link")
        z.extractall(destination)
    print("Extracted",archive.name,flush=True)
analyzer=D4J/"framework/lib/build-analyzer-0.0.1.jar"
if not analyzer.exists():
    urllib.request.urlretrieve("https://github.com/jose/build-analyzer/releases/download/v0.0.1/build-analyzer-0.0.1.jar",analyzer)
# Same contents as official init.sh's analyzer.jar symlink; a regular copy is portable.
shutil.copyfile(analyzer,D4J/"framework/lib/analyzer.jar")
print("Analyzer installed; verify defects4j info before claiming setup passed")
