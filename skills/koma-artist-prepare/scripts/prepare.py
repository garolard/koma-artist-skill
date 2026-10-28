#!/usr/bin/env python3
"""Copy a KOMA set plan into a new Studio bulk-import folder."""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def prepare(plan_path: Path, output: Path) -> int:
    plan_path = plan_path.resolve(strict=True)
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    if not isinstance(plan, dict) or not isinstance(plan.get('panels'), list) or not plan['panels']:
        raise ValueError('Plan must contain a non-empty panels array.')
    panels = plan['panels']
    if len(panels) > 49:
        raise ValueError('A standard set has at most 49 panels.')
    if output.exists() or output.is_symlink():
        raise ValueError(f'Output already exists: {output}')
    prepared = []
    sources = set()
    names = set()
    for index, panel in enumerate(panels, 1):
        if not isinstance(panel, dict) or type(panel.get('slot')) is not int or panel['slot'] != index:
            raise ValueError(f'Panels must be ordered with consecutive slots starting at 1 (expected {index}).')
        source, title = panel.get('source'), panel.get('title')
        if not isinstance(source, str) or not source.strip() or not isinstance(title, str) or not title.strip():
            raise ValueError(f'Panel {index} needs a source and title.')
        title = title.strip()
        if len(title) > 60 or any(ord(c) < 32 for c in title) or any(c in title for c in '/\\:*?"<>|'):
            raise ValueError(f'Panel {index} has an invalid title; use 1–60 characters without path separators or control characters.')
        # Studio removes leading numbers and separators and changes underscores to spaces.
        if re.match(r'^[\d\s._-]', title) or '_' in title or '-' in title:
            raise ValueError(f'Panel {index} title cannot start with digits or separators or contain hyphens or underscores; Studio would change it.')
        path = Path(source).expanduser()
        path = (plan_path.parent / path).resolve(strict=True) if not path.is_absolute() else path.resolve(strict=True)
        if not path.is_file() or not path.suffix:
            raise ValueError(f'Panel {index} source must be a file with an extension: {source}')
        if path in sources:
            raise ValueError(f'Panel {index} repeats a source file: {source}')
        name = f'{index:02d} - {title}{path.suffix.lower()}'
        if name.casefold() in names:
            raise ValueError(f'Filename collision: {name}')
        sources.add(path)
        names.add(name.casefold())
        prepared.append((path, name))
    output.mkdir(parents=False, exist_ok=False)
    try:
        for source, name in prepared:
            shutil.copyfile(source, output / name)
    except Exception:
        shutil.rmtree(output)
        raise
    print(f'Copied {len(prepared)} panels to {output}. Drag its contents into an empty Studio draft.')
    print('Studio guesses shapes and crops; review framing and assign rarities, cover and previews separately.')
    print('Browser image format support varies; check the Studio import queue for failures.')
    return len(prepared)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path, help='JSON plan; relative source paths are relative to this file')
    parser.add_argument('output', type=Path, help='new panel directory; its parent must already exist')
    args = parser.parse_args()
    try:
        prepare(args.plan, args.output)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'Preparation failed: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
