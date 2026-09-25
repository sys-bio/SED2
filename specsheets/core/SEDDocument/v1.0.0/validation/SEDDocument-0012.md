---
id: SEDDocument-0012
rule: "No JSON object in a SED2 document may contain the same key more than once."
message: "Key '{attr}' appears more than once at '{location}'."
severity: error
status: active
---

JSON parsers silently keep one copy of a duplicated key (usually the last),
so a document with two tasks named sim1 would lose one without any error.
Needs a parser-level hook in each language: Python's object_pairs_hook,
Jackson's STRICT_DUPLICATE_DETECTION, and a parse callback for nlohmann.
