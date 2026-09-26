---
id: AbstractReport-0001
rule: The format attribute of an AbstractReport, if present, must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`format` is optional; when present, it must be a string.
