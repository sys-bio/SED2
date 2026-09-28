#!/usr/bin/env python3
"""SED2 generator CLI. See Design.md's Code Generation / Repository Layout.

Usage:
    python3 generator/generate.py --spec-root test-specsheets \
        --out test-specsheets/generated --doc-class TestDocument --base-mixin TestBase \
        --lang python,java,cpp
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.spec import load_spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--doc-class", required=True)
    ap.add_argument("--base-mixin", required=True)
    ap.add_argument("--lang", default="python,java,cpp")
    ap.add_argument("--rules-version", default="v1.0.0")
    args = ap.parse_args()

    model = load_spec(args.spec_root, document_class_hint=args.doc_class)
    model.base_mixin = args.base_mixin

    os.makedirs(args.out, exist_ok=True)
    schema_dir = os.path.join(args.out, "schema")
    os.makedirs(schema_dir, exist_ok=True)
    rules_out = {
        rid: {
            "class": rid.split("-")[0],
            "rule": r.rule,
            "message": r.message,
            "severity": r.severity,
            "status": r.status,
            "check": r.check,
        }
        for rid, r in sorted(model.rules.items())
    }
    with open(os.path.join(args.out, f"rules-{args.rules_version}.json"), "w") as f:
        json.dump(rules_out, f, indent=2)
        f.write("\n")

    langs = args.lang.split(",")
    if "python" in langs:
        from generator.emit_python import emit_python_package
        emit_python_package(model, os.path.join(args.out, "python"))
        print(f"[generate] wrote Python package to {os.path.join(args.out, 'python')}")
    if "java" in langs:
        from generator.emit_java import emit_java_package
        emit_java_package(model, os.path.join(args.out, "java"))
        print(f"[generate] wrote Java package to {os.path.join(args.out, 'java')}")
    if "cpp" in langs:
        from generator.emit_cpp import emit_cpp_package
        emit_cpp_package(model, os.path.join(args.out, "cpp"))
        print(f"[generate] wrote C++ package to {os.path.join(args.out, 'cpp')}")

    print(f"[generate] classes: {sorted(model.generatable_classes())}")
    print(f"[generate] rules: {len(model.rules)}")


if __name__ == "__main__":
    main()
