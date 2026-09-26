---
id: SEDDocument-0011
rule: "The version of a SEDDocument should not be newer than the newest document version this library knows."
message: "Document version '{value}' is newer than the newest version this library supports ('{max}'); newer features may be reported as errors."
severity: warning
status: active
check: handwritten
---

Version resolution picks the newest directory not greater than the
document's version, so a v1.3.0 document silently validates against v1.2.x
rules. This makes that visible.
