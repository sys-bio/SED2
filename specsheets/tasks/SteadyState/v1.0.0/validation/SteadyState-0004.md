---
id: SteadyState-0004
rule: The independentVariable attribute of a SteadyState, if present, must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`independentVariable` is `StringOrRef`, which resolves to a plain string type; when present, it must be a string.
