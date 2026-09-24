---
id: Repeat-0003
rule: When the value of outputVariableMap of a Repeat is a reference, it must be a reference to an object whose values are SIdRef.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an object whose values are SIdRef."
severity: error
status: active
---

`outputVariableMap` is `object (values: SIdRef) or SIdRef` in Repeat: when the value is a reference, it must resolve to an object whose values are SIdRef.
