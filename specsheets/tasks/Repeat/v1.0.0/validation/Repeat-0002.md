---
id: Repeat-0002
rule: When the value of outputVariableMap of a Repeat is provided directly, it must be an object whose values are SIdRef.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are SIdRef."
severity: error
status: active
---

`outputVariableMap` is `object (values: SIdRef) or SIdRef` in Repeat: the value, when not a reference, must be an object whose values are SIdRef.
