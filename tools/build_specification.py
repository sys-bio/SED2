#!/usr/bin/env python3
"""Assemble core-spec.md + every specsheets/ Data Sheet into a single SPECIFICATION.md.

This is a generated file: never hand-edit SPECIFICATION.md directly, re-run this
script instead. It reads:
  - core-spec.md           (the document overview, sections 1-N)
  - specsheets/<category>/<ClassName>/<version>/description.md   (one per class)
  - specsheets/<category>/<ClassName>/<version>/validation/*.md   (numbered rules)
  - model_formats/<Format>/description.md, its topic files (labels.md, setValues.md,
    modelChange.md, elementTypes.md, jacobian.md, steadyState.md, ...) and validation/*.md; each model format
    becomes its own Appendix after the Class Reference
and writes a single self-contained SPECIFICATION.md at the repo root, with
relative image links rewritten to resolve from the repo root and
description-to-description cross-references rewritten to in-document anchors,
so the result reads as one document on GitHub and converts cleanly with
pandoc (see the invocations printed at the end of a run).

Bread crumbs: every section of core-spec.md, every class, and every validation rule
gets a "Source:" link back to the .md file it was assembled from (repo-root-relative,
with a #L<line> anchor where a single line is meaningful), so a reader of the
assembled document can jump straight to the file to edit.

The output is deterministic (no date or other run-dependent content), so CI can
regenerate it on every run and commit only when it actually changed.

Usage: python3 tools/build_specification.py [--repo-root PATH]
"""
import argparse
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

# Topic files of a model format, in the order they appear in its Appendix, with the
# title each gets. Any other .md file in a format's folder (except description.md)
# is appended afterwards, alphabetically, titled after its file name.
FORMAT_TOPICS = [
    ("labels.md", "Labels"),
    ("setValues.md", "setValues"),
    ("modelChange.md", "ModelChange"),
    ("elementTypes.md", "Element types"),
    ("jacobian.md", "Jacobian"),
    ("steadyState.md", "SteadyState"),
]


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


def discover_model_formats(model_formats_root):
    """Return [(format_name, format_dir), ...] sorted alphabetically (case-insensitive).

    A model format is any subdirectory of model_formats/ holding a description.md."""
    formats = []
    if os.path.isdir(model_formats_root):
        for name in sorted(os.listdir(model_formats_root), key=str.lower):
            d = os.path.join(model_formats_root, name)
            if os.path.isdir(d) and os.path.isfile(os.path.join(d, "description.md")):
                formats.append((name, d))
    return formats


def format_topics(format_dir):
    """Return [(filename, title), ...] for a model format's topic files, in order."""
    known = [(fn, title) for fn, title in FORMAT_TOPICS if os.path.isfile(os.path.join(format_dir, fn))]
    known_names = {fn for fn, _ in known}
    extra = sorted(
        f for f in os.listdir(format_dir)
        if f.endswith(".md") and f != "description.md" and f not in known_names
        and os.path.isfile(os.path.join(format_dir, f))
    )
    return known + [(fn, os.path.splitext(fn)[0]) for fn in extra]


def appendix_letter(index):
    """0 -> A, 1 -> B, ... (past Z: AA, AB, ...)."""
    letters = ""
    n = index
    while True:
        letters = chr(ord("A") + n % 26) + letters
        n = n // 26 - 1
        if n < 0:
            return letters


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


def source_link(rel_path, line=None):
    """A bread crumb pointing back at a source .md file (optionally at one line of it)."""
    if line is None:
        return f"*Source: [{rel_path}]({rel_path})*"
    return f"*Source: [{rel_path}, line {line}]({rel_path}#L{line})*"


def add_heading_breadcrumbs(md_text, rel_path):
    """After every level-2 ('## ') heading, add a bread crumb to that line of rel_path.

    Must run on the source text before any heading shifting or first-line dropping,
    so the line numbers are the file's real ones. Skips fenced code blocks."""
    out = []
    in_fence = False
    for lineno, line in enumerate(md_text.split("\n"), start=1):
        out.append(line)
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^##\s+", line):
            out.append("")
            out.append(source_link(rel_path, lineno))
            out.append("")
    return "\n".join(out)


def render_validation(validation_dir, rel_dir, rewrite, heading="##### Validation Rules"):
    """Render a class's numbered rules. rel_dir is the version dir relative to the repo root
    (for the bread crumbs); rewrite is applied to rule text/bodies to fix up their links."""
    if not os.path.isdir(validation_dir):
        return ""
    files = sorted(f for f in os.listdir(validation_dir) if f.endswith(".md"))
    if not files:
        return ""
    parts = [heading + "\n"]
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
        crumb = f"([source]({rel_dir}/validation/{fn}))"
        parts.append(rewrite(f"**`{rule_id}`** ({severity}) - {rule}") + f" {crumb}\n")
        if body:
            quoted = "\n".join(f"> {line}" if line else ">" for line in body.split("\n"))
            parts.append(rewrite(quoted) + "\n")
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
    model_formats = discover_model_formats(os.path.join(root, "model_formats"))

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

    # Appendix headings (one per model format) and their topic headings.
    appendix_title = {}
    appendix_anchor = {}
    topic_anchor = {}
    for i, (fmt_name, fmt_dir) in enumerate(model_formats):
        appendix_title[fmt_name] = f"Appendix {appendix_letter(i)}: {fmt_name}"
        appendix_anchor[fmt_name] = slugify(appendix_title[fmt_name])
        for fn, title in format_topics(fmt_dir):
            topic_anchor[(fmt_name, fn)] = slugify(f"{title} ({fmt_name})")

    with open(core_spec_path, encoding="utf-8") as f:
        core_spec_text = f.read()
    # core-spec.md's own "# SED2 Core Specification" -> "## Core Specification" (shift +1),
    # and its "## N. ..." sections become "### N. ...".
    core_spec_text = add_heading_breadcrumbs(core_spec_text, "core-spec.md")
    core_spec_text = drop_first_heading(core_spec_text)
    core_spec_text = shift_headings(core_spec_text, 1)
    core_spec_anchor = slugify("Core Specification")

    out = []
    out.append("---")
    out.append("title: SED2 Specification")
    out.append("---")
    out.append("")
    out.append("# SED2 Specification")
    out.append("")
    out.append(
        "*This file is generated by `tools/build_specification.py` from `core-spec.md` "
        "and every Data Sheet under `specsheets/`. Do not hand-edit it - re-run the "
        "script instead.*"
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
    for fmt_name, fmt_dir in model_formats:
        out.append(f"- [{appendix_title[fmt_name]}](#{appendix_anchor[fmt_name]})")
        for fn, title in format_topics(fmt_dir):
            out.append(f"    - [{title} ({fmt_name})](#{topic_anchor[(fmt_name, fn)]})")
    out.append("")
    out.append("---")
    out.append("")

    # --- Core Specification section ---
    out.append("## Core Specification")
    out.append("")
    out.append(source_link("core-spec.md"))
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
            out.append(source_link(f"{rel_dir}/description.md"))
            out.append("")
            out.append(desc_text.strip())
            out.append("")

            validation_dir = os.path.join(version_dir, "validation")
            validation_md = render_validation(
                validation_dir,
                rel_dir,
                lambda text: rewrite_links(text, rel_dir, anchor_by_class_relpath),
            )
            if validation_md:
                out.append(validation_md.strip())
                out.append("")
        out.append("---")
        out.append("")

    # --- Appendices: one per model format ---
    for fmt_name, fmt_dir in model_formats:
        rel_dir = os.path.relpath(fmt_dir, root).replace(os.sep, "/")
        rewrite = lambda text, rel_dir=rel_dir: rewrite_links(text, rel_dir, anchor_by_class_relpath)

        out.append(f"## {appendix_title[fmt_name]}")
        out.append("")
        out.append(source_link(f"{rel_dir}/description.md"))
        out.append("")
        with open(os.path.join(fmt_dir, "description.md"), encoding="utf-8") as f:
            desc_text = f.read()
        desc_text = add_heading_breadcrumbs(desc_text, f"{rel_dir}/description.md")
        desc_text = drop_first_heading(desc_text)
        desc_text = shift_headings(desc_text, 2)
        out.append(rewrite(desc_text.strip()))
        out.append("")

        for fn, title in format_topics(fmt_dir):
            with open(os.path.join(fmt_dir, fn), encoding="utf-8") as f:
                topic_text = f.read()
            topic_text = add_heading_breadcrumbs(topic_text, f"{rel_dir}/{fn}")
            topic_text = drop_first_heading(topic_text)
            topic_text = shift_headings(topic_text, 2)  # "## X" -> "#### X"
            out.append(f"### {title} ({fmt_name})")
            out.append("")
            out.append(source_link(f"{rel_dir}/{fn}"))
            out.append("")
            out.append(rewrite(topic_text.strip()))
            out.append("")

        validation_md = render_validation(
            os.path.join(fmt_dir, "validation"),
            rel_dir,
            rewrite,
            heading=f"### Validation Rules ({fmt_name})",
        )
        if validation_md:
            out.append(validation_md.strip())
            out.append("")
        out.append("---")
        out.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")

    print(f"Wrote {out_path}")
    print(f"  {len(sum(classes_by_category.values(), []))} classes across {len(CATEGORIES)} categories")
    print(f"  {len(model_formats)} model format appendices")
    print("")
    print("To convert with pandoc (from the repo root, so relative image paths resolve):")
    print("  pandoc SPECIFICATION.md -o SPECIFICATION.html --standalone --toc --resource-path=.")
    print("  pandoc SPECIFICATION.md -o SPECIFICATION.pdf --toc --resource-path=.")


if __name__ == "__main__":
    main()
