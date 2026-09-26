---
id: Choice-0003
rule: The label attribute of a Choice, if present, must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`label` is optional; when present, it must be a string.
