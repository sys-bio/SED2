---
id: ModelChange-0003
rule: When the value of setValues of a ModelChange is provided directly, it must be an object whose values are AnyValueOrRef.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AnyValueOrRef."
severity: error
status: active
check: schema
---

`setValues` is `object (values: AnyValueOrRef) or SIdRef`: the value, when not a reference, must be an object whose values are AnyValueOrRef.
