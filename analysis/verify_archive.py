#!/usr/bin/env python3
"""Verify the exact source and data bytes declared for the reproducibility archive.

Run before regeneration; generated outputs may differ in harmless renderer or
floating-point serialization details. This integrity check does not establish
the truth of author-held historical custody records.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'ARCHIVE_MANIFEST.json'


def main():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if manifest['schema'] != 'reproducibility_archive_manifest_v1':
        raise SystemExit('Unsupported archive manifest schema')
    files = manifest['files']
    for name, expected in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name:
            raise SystemExit('Invalid archive member: ' + name)
        target = ROOT.joinpath(*path.parts)
        if target.is_symlink():
            raise SystemExit('Archive members must be regular files: ' + name)
        content = target.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest != expected['sha256'] or len(content) != expected['bytes']:
            raise SystemExit('Archive identity mismatch: ' + name)
        print(name, digest, len(content), 'PASS')
    # A source checkout must contain exactly the declared tracked tree. Running
    # from a downloaded source archive still checks every declared file above.
    if (ROOT / '.git').exists():
        tracked = set(subprocess.check_output(
            ['git', 'ls-files'], cwd=ROOT, text=True).splitlines())
        if tracked != set(files) | {'ARCHIVE_MANIFEST.json'}:
            raise SystemExit('Tracked tree differs from archive manifest')
    print(f'Archive identities: {len(files)} files PASS; manifest excluded from its own digest')


if __name__ == '__main__':
    main()
