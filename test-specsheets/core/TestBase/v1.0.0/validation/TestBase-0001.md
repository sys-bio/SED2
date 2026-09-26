---
id: TestBase-0001
rule: The name attribute of a TestBase-derived element, if present, must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`name` is optional; when present, it must be a string. Mirrors `specsheets/core/SEDBase`'s `SEDBase-0001`.
