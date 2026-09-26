---
id: Report-0002
rule: The data attribute of a Report, if present, must be a reference (a string starting with '#').
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a reference."
severity: error
status: active
check: schema
---

`data` is `SIdRef` - always a reference, never a literal value.
