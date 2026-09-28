---
id: TypesWidget-0006
rule: The primaryNote attribute of a TypesWidget, if present, must be a Note object.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a Note object."
severity: error
status: active
check: schema
---

`primaryNote` is optional; when present it must be a single embedded `Note` object. Problems inside the Note itself (for example a missing `text`) are reported under the Note's own rules, not this one.
