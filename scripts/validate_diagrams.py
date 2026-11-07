#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate generated diagram files and Markdown/data diagram references.

Diagrams are PNG (hand-built) and GIF (trace animations). The validator
rejects any leftover SVG artefacts or model-placeholder names so the old
SVG/-model pipeline cannot sneak back.
"""
from pathlib import Path
import json
import re
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "assets" / "diagrams"
CHAPTERS = ROOT / "chapters"
PROBLEMS = ROOT / "data" / "problems.json"

errors = []
image_files = sorted(
    p for p in DIAGRAMS.iterdir() if p.suffix.lower() in {".png", ".gif"}
)
stale_svg = sorted(DIAGRAMS.glob("*.svg"))
if stale_svg:
    errors.append("stale SVG files on disk: " + ", ".join(p.name for p in stale_svg))

for path in image_files:
    try:
        with Image.open(path) as im:
            im.verify()
        if path.suffix.lower() == ".gif":
            with Image.open(path) as im:
                if getattr(im, "n_frames", 1) < 2:
                    errors.append(f"{path.name}: trace GIF has a single frame")
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
explained = 0
for problem in problems:
    solution = problem.get("solution", {})
    understanding = solution.get("understanding", {})
    if understanding.get("trace") and understanding.get("why_correct"):
        explained += 1
    diagram = understanding.get("diagram") or solution.get("diagram")
    if not diagram:
        errors.append(f"{problem['id']}: missing diagram")
        continue
    diagrammed += 1
    src = diagram["src"]
    if "-model." in src or src.endswith(".svg"):
        errors.append(f"{problem['id']}: legacy diagram reference {src}")
    source = Path(src.removeprefix("./"))
    if not source.is_file():
        errors.append(f"{problem['id']}: missing {src}")
    referenced.add(source.name)

if explained != len(problems):
    errors.append(f"five-question coverage {explained}/{len(problems)}, expected full coverage")

unused = sorted(path.name for path in image_files if path.name not in referenced)
if unused:
    errors.append("unreferenced diagram files: " + ", ".join(unused))

print(f"diagram files: {len(image_files)} ({sum(1 for p in image_files if p.suffix == '.gif')} GIF)")
print(f"referenced diagram files: {len(referenced & {p.name for p in image_files})}")
print(f"problem diagrams: {diagrammed}")
print("validation: ok" if not errors else "validation: failed")
for error in errors:
    print(error)
sys.exit(bool(errors))
