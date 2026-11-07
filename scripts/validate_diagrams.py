#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate generated SVG files and Markdown/data diagram references."""
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "assets" / "diagrams"
CHAPTERS = ROOT / "chapters"
PROBLEMS = ROOT / "data" / "problems.json"

errors = []
svg_files = sorted(DIAGRAMS.glob("*.svg"))
for path in svg_files:
    try:
        root = ET.parse(path).getroot()
        if root.tag != "{http://www.w3.org/2000/svg}svg":
            errors.append(f"{path.name}: root is not SVG")
    except Exception as exc:
        errors.append(f"{path.name}: {exc}")

referenced = set()
for path in CHAPTERS.glob("*.md"):
    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        source = Path(match.group(1).removeprefix("./"))
        if not source.is_file():
            errors.append(f"{path.name}: missing {match.group(1)}")
        referenced.add(source.name)

problems = json.loads(PROBLEMS.read_text(encoding="utf-8"))
diagrammed = 0
for problem in problems:
    solution = problem.get("solution", {})
    diagram = solution.get("understanding", {}).get("diagram") or solution.get("diagram")
    if not diagram:
        continue
    diagrammed += 1
    source = Path(diagram["src"].removeprefix("./"))
    if not source.is_file():
        errors.append(f"{problem['id']}: missing {diagram['src']}")
    referenced.add(source.name)

unused = sorted(path.name for path in svg_files if path.name not in referenced)
if unused:
    errors.append("unreferenced SVG files: " + ", ".join(unused))

print(f"SVG files: {len(svg_files)}")
print(f"chapter diagram references: {len(referenced & {p.name for p in svg_files})}")
print(f"problem diagrams: {diagrammed}")
print("validation: ok" if not errors else "validation: failed")
for error in errors:
    print(error)
sys.exit(bool(errors))
