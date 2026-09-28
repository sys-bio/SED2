---
id: TypesWidget-0007
rule: The extras attribute of a TypesWidget, if present, must be an object whose keys are SIds.
message: "Attribute '{attr}' of {class} '{id}' is not an object keyed by valid SIds."
severity: error
status: active
check: schema
---

`extras` is optional; when present it must be a JSON object whose keys are valid SIds. Values are unconstrained (any JSON value or reference).
