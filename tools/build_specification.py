#!/usr/bin/env python3
"""Assemble core-spec.md + every specsheets/ Data Sheet into a single SPECIFICATION.md.

This is a generated file: never hand-edit SPECIFICATION.md directly, re-run this
script instead. It reads:
  - core-spec.md           (the document overview, sections 1-N)
  - specsheets/<category>/<ClassName>/<version>/description.md   (one per class)
  - specsheets/<category>/<ClassName>/<version>/validation/*.md   (numbered rules)
and writes a single self-contained SPECIFICATION.md at the repo root, with
relative image links rewritten to resolve from the repo root and
description-to-description cross-references rewritten to in-document anchors,
so the result reads as one document on GitHub and converts cleanly with
pandoc (see the invocations printed at the end of a run).

Usage: python3 tools/build_specification.py [--repo-root PATH]
"""
import argparse
import datetime
import os
import re
import sys

CATEGORIES = ["core", "tasks", "outputs", "auxiliary"]
CATEGORY_TITLES = {
    "core": "Core Classes",
    "tasks": "Task Classes",
    "outputs": "Output Classes",
    "auxiliary": "Auxiliary Classes",
}


def find_latest_version_dir(class_dir):
    """Pick the highest vX.Y.Z directory under a class's folder."""
    versions = []
    for name in os.listdir(class_dir):
        m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", name)
        if m and os.path.isdir(os.path.join(class_dir, name)):
            versions.append((tuple(int(g) for g in m.groups()), name))
    if not versions:
        return None
    versions.sort()
    return versions[-1][1]


def discover_classes(specsheets_root):
    """Return {category: [(class_name, version_dir_path), ...]} sorted alphabetically."""
    result = {}
    for category in CATEGORIES:
        cat_dir = os.path.join(specsheets_root, category)
        classes = []
        if os.path.isdir(cat_dir):
            for class_name in sorted(os.listdir(cat_dir), key=str.lower):
                class_dir = os.path.join(cat_dir, class_name)
                if not os.path.isdir(class_dir):
                    continue
                version = find_latest_version_dir(class_dir)
                if version is None:
                    continue
                classes.append((class_name, os.path.join(class_dir, version)))
        result[category] = classes
    return result


_slug_used = {}


def reset_slugs():
    _slug_used.clear()


def slugify(text):
    """Approximate GitHub's heading-anchor slug algorithm."""
    s = text.strip().lower()
    s = re.sub(r"`", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = s.strip("-")
    if s in _slug_used:
        _slug_used[s] += 1
        return f"{s}-{_slug_used[s]}"
    _slug_used[s] = 0
    return s


def shift_headings(md_text, shift):
    """Increase every ATX heading's level by `shift` (## -> #### for shift=2), skipping fenced code blocks."""
    lines = md_text.split("\n")
    out = []
    in_fence = False
    for line in lines:
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})(\s+.*)$", line)
            if m:
                level = len(m.group(1))
                new_level = min(level + shift, 6)
                out.append("#" * new_level + m.group(2))
                continue
        out.append(line)
    return "\n".join(out)


def drop_first_heading(md_text):
    """Remove the first line if it's a level-1 '# ClassName' heading (redundant - we emit our own)."""
    lines = md_text.split("\n", 1)
    if lines and re.match(r"^#\s+", lines[0]):
        return lines[1].lstrip("\n") if len(lines) > 1 else ""
    return md_text


def rewrite_links(md_text, class_rel_dir, anchor_by_class_relpath):
    """Rewrite same-folder file links to repo-root-relative paths, and
    description.md cross-references to in-document anchors."""

    def repl(m):
        target = m.group(1)
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            return m.group(0)
        # Resolve the link relative to the class's own folder, to a repo-root-relative path.
        resolved = os.path.normpath(os.path.join(class_rel_dir, target)).replace(os.sep, "/")
        if resolved in anchor_by_class_relpath:
            return f"](#{anchor_by_class_relpath[resolved]})"
        return f"]({resolved})"

    return re.sub(r"\]\(([^)]+)\)", repl, md_text)


def render_validation(validation_dir):
    if not os.path.isdir(validation_dir):
        return ""
    files = sorted(f for f in os.listdir(validation_dir) if f.endswith(".md"))
    if not files:
        return ""
    parts = ["##### Validation Rules\n"]
    for fn in files:
        with open(os.path.join(validation_dir, fn), encoding="utf-8") as f:
            text = f.read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
        if not m:
            continue
        frontmatter, body = m.group(1), m.group(2).strip()
        fields = {}
        for line in frontmatter.split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                fields[k.strip()] = v.strip().strip('"')
        rule_id = fields.get("id", fn)
        rule = fields.get("rule", "")
        severity = fields.get("severity", "")
        parts.append(f"**`{rule_id}`** ({severity}) - {rule}\n")
        if body:
            quoted = "\n".join(f"> {line}" if line else ">" for line in body.split("\n"))
            parts.append(quoted + "\n")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=os.getcwd())
    args = ap.parse_args()
    root = os.path.abspath(args.repo_root)
    specsheets_root = os.path.join(root, "specsheets")
    core_spec_path = os.path.join(root, "core-spec.md")
    out_path = os.path.join(root, "SPECIFICATION.md")

    if not os.path.isdir(specsheets_root):
        print(f"error: {specsheets_root} not found", file=sys.stderr)
        sys.exit(1)

    classes_by_category = discover_classes(specsheets_root)

    reset_slugs()
    # Pre-register anchors for every class so cross-references can resolve
    # regardless of which class is processed first.
    anchor_by_class_relpath = {}
    class_anchor = {}
    for category in CATEGORIES:
        for class_name, version_dir in classes_by_category[category]:
            rel_dir = os.path.relpath(version_dir, root).replace(os.sep, "/")
            desc_relpath = f"{rel_dir}/description.md"
            anchor = slugify(class_name)
            anchor_by_class_relpath[desc_relpath] = anchor
            class_anchor[(category, class_name)] = anchor

    with open(core_spec_path, encoding="utf-8") as f:
        core_spec_text = f.read()
    # core-spec.md's own "# SED2 Core Specification" -> "## Core Specification" (shift +1),
    # and its "## N. ..." sections become "### N. ...".
    core_spec_text = drop_first_heading(core_spec_text)
    core_spec_text = shift_headings(core_spec_text, 1)
    core_spec_anchor = slugify("Core Specification")

    today = datetime.date.today().isoformat()

    out = []
    out.append("---")
    out.append("title: SED2 Specification")
    out.append(f"date: {today}")
    out.append("---")
    out.append("")
    out.append("# SED2 Specification")
    out.append("")
    out.append(
        "*This file is generated by `tools/build_specification.py` from `core-spec.md` "
        "and every Data Sheet under `specsheets/`. Do not hand-edit it - re-run the "
        f"script instead. Generated: {today}.*"
    )
    out.append("")

    # --- Table of contents ---
    out.append("## Table of Contents")
    out.append("")
    out.append(f"- [Core Specification](#{core_spec_anchor})")
    for line in core_spec_text.split("\n"):
        m = re.match(r"^###\s+(.*)$", line)
        if m:
            title = m.group(1)
            out.append(f"    - [{title}](#{slugify(title)})")
    class_ref_anchor = slugify("Class Reference")
    out.append(f"- [Class Reference](#{class_ref_anchor})")
    for category in CATEGORIES:
        cat_title = CATEGORY_TITLES[category]
        out.append(f"    - [{cat_title}](#{slugify(cat_title)})")
        for class_name, _ in classes_by_category[category]:
            out.append(f"        - [{class_name}](#{class_anchor[(category, class_name)]})")
    out.append("")
    out.append("---")
    out.append("")

    # --- Core Specification section ---
    out.append("## Core Specification")
    out.append("")
    out.append(core_spec_text.strip())
    out.append("")
    out.append("---")
    out.append("")

    # --- Class Reference ---
    out.append("## Class Reference")
    out.append("")
    for category in CATEGORIES:
        out.append(f"### {CATEGORY_TITLES[category]}")
        out.append("")
        for class_name, version_dir in classes_by_category[category]:
            rel_dir = os.path.relpath(version_dir, root).replace(os.sep, "/")
            desc_path = os.path.join(version_dir, "description.md")
            if not os.path.isfile(desc_path):
                continue
            with open(desc_path, encoding="utf-8") as f:
                desc_text = f.read()
            desc_text = drop_first_heading(desc_text)
            desc_text = shift_headings(desc_text, 3)  # class's own "## X" -> "##### X", "### Y" -> "###### Y"
            desc_text = rewrite_links(desc_text, rel_dir, anchor_by_class_relpath)

            out.append(f"#### {class_name}")
            out.append("")
            out.append(desc_text.strip())
            out.append("")

            validation_dir = os.path.join(version_dir, "validation")
            validation_md = render_validation(validation_dir)
            if validation_md:
                validation_md = rewrite_links(validation_md, rel_dir, anchor_by_class_relpath)
                out.append(validation_md.strip())
                out.append("")
        out.append("---")
        out.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")

    print(f"Wrote {out_path}")
    print(f"  {len(sum(classes_by_category.values(), []))} classes across {len(CATEGORIES)} categories")
    print("")
    print("To convert with pandoc (from the repo root, so relative image paths resolve):")
    print("  pandoc SPECIFICATION.md -o SPECIFICATION.html --standalone --toc --resource-path=.")
    print("  pandoc SPECIFICATION.md -o SPECIFICATION.pdf --toc --resource-path=.")


if __name__ == "__main__":
    main()
