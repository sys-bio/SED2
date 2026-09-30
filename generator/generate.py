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
    ap.add_argument("--python-package", default="libsed2test",
                     help="Python distribution/import package name (default: libsed2test, the Phase-1 test-tree name)")
    ap.add_argument("--python-description", default=None,
                     help="pyproject.toml [project] description; defaults to the Phase-1 test-tree description")
    ap.add_argument("--java-package", default="org.sed2test",
                     help="Java package name (default: org.sed2test, the Phase-1 test-tree name)")
    ap.add_argument("--java-group-id", default=None,
                     help="Maven groupId; defaults to --java-package")
    ap.add_argument("--java-artifact-id", default="libsed2test",
                     help="Maven artifactId (default: libsed2test, the Phase-1 test-tree name)")
    ap.add_argument("--java-description", default=None,
                     help="pom.xml <description>; defaults to the Phase-1 test-tree description")
    ap.add_argument("--cpp-namespace", default="sed2test",
                     help="C++ namespace / CMake project+target name (default: sed2test, the Phase-1 test-tree name)")
    ap.add_argument("--no-gen-fixtures", action="store_true",
                     help="Skip schema-derivable fixture generation (fixtures/generated/ next to --out's parent) - "
                          "on by default whenever Python is in --lang, since verification needs the Python library")
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
        emit_python_package(
            model, os.path.join(args.out, "python"),
            package_name=args.python_package,
            description=args.python_description,
        )
        print(f"[generate] wrote Python package '{args.python_package}' to {os.path.join(args.out, 'python')}")
        if not args.no_gen_fixtures:
            from generator.gen_fixtures import generate_schema_fixtures, verify_and_write
            fixtures = generate_schema_fixtures(model)
            fixtures_out = os.path.join(os.path.dirname(os.path.normpath(args.out)) or ".", "fixtures", "generated")
            verify_and_write(fixtures, fixtures_out, os.path.join(args.out, "python"), args.python_package)
            # ref-type tier (formulaic "if a reference, must resolve to type X" rules) -
            # only for a spec that has some (the synthetic test tree has none).
            if any(r.check == "ref-type" for r in model.rules.values()):
                from generator import gen_reftype_fixtures as _reftype
                _reftype.verify_and_write(
                    _reftype.generate_reftype_fixtures(model),
                    fixtures_out, os.path.join(args.out, "python"), args.python_package)
    if "java" in langs:
        from generator.emit_java import emit_java_package
        emit_java_package(
            model, os.path.join(args.out, "java"),
            java_package=args.java_package,
            maven_group_id=args.java_group_id,
            maven_artifact_id=args.java_artifact_id,
            description=args.java_description,
        )
        print(f"[generate] wrote Java package '{args.java_package}' to {os.path.join(args.out, 'java')}")
    if "cpp" in langs:
        from generator.emit_cpp import emit_cpp_package
        emit_cpp_package(
            model, os.path.join(args.out, "cpp"),
            cpp_namespace=args.cpp_namespace,
        )
        print(f"[generate] wrote C++ package '{args.cpp_namespace}' to {os.path.join(args.out, 'cpp')}")

    print(f"[generate] classes: {sorted(model.generatable_classes())}")
    print(f"[generate] rules: {len(model.rules)}")


if __name__ == "__main__":
    main()
