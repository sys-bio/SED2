"""Top-level read/write entry points for libsed2. GENERATED."""
from __future__ import annotations
import json
from .model import SEDDocument, _load_fields


def read_from_string(text: str) -> "SEDDocument":
    raw = json.loads(text)
    obj = SEDDocument()
    _load_fields(obj, raw)
    obj._attach(None, obj)
    return obj


def read_from_file(path: str) -> "SEDDocument":
    with open(path, "r", encoding="utf-8") as f:
        return read_from_string(f.read())


def write_to_string(doc: "SEDDocument") -> str:
    return json.dumps(doc.to_json_value(), indent=2)


def write_to_file(doc: "SEDDocument", path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(write_to_string(doc))
