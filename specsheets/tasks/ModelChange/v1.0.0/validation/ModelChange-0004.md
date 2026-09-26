---
id: ModelChange-0004
rule: When the value of setValues of a ModelChange is a reference, it must be a reference to an object whose values are AnyValueOrRef.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an object whose values are AnyValueOrRef."
severity: error
status: active
check: ref-type
---

`setValues` is `object (values: AnyValueOrRef) or SIdRef`: when the value is a reference, it must resolve to an object whose values are AnyValueOrRef.
