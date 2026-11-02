"""Create or verify a supplemental transfer ZIP; no credentials or environment installs."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs/migration'
SOURCES = ('inputs', 'work/dependencies', 'work/course-reading', 'work/syllabus-review')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true', help='Verify files after extraction')
    args = parser.parse_args()
    manifest_path = ROOT / 'outputs/migration-files.json'
    if args.verify:
        data = json.loads(manifest_path.read_text(encoding='utf-8'))
        failures = [f['path'] for f in data['files']
                    if not (ROOT/f['path']).is_file() or digest(ROOT/f['path']) != f['sha256']]
        if failures:
            raise SystemExit('Missing/changed transfer files: ' + ', '.join(failures))
        print(f"Verified {len(data['files'])} transfer files")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / 'sqa-transfer-supplement.zip'
    if target.exists():
        raise SystemExit('Transfer ZIP already exists; preserve it or choose a new snapshot location')
    records = []
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for source in SOURCES:
            for path in sorted((ROOT/source).rglob('*')):
                if path.is_symlink() or not path.is_file():
                    continue
                relative = path.relative_to(ROOT).as_posix()
                records.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': digest(path)})
                archive.write(path, relative)
        archive.writestr('TRANSFER_CONTENTS.json', json.dumps(records, indent=2, ensure_ascii=False))
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise SystemExit('ZIP CRC verification failed')
    manifest_path.write_text(json.dumps({'files': records, 'archive_sha256': digest(target),
                                        'archive_bytes': target.stat().st_size}, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Created and CRC-verified {target}: {target.stat().st_size:,} bytes, {len(records)} files')

if __name__ == '__main__':
    main()
