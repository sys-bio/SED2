---
id: TestDocument-0003
rule: The reports attribute of a TestDocument, if present, must be an object whose values are AbstractReport objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractReport objects."
severity: error
status: active
check: schema
---

`reports` is optional; when present, each value must resolve to a concrete `AbstractReport` branch.
