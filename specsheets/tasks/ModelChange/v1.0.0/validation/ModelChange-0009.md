---
id: ModelChange-0009
rule: When the value of replaceElements of a ModelChange is provided directly, it must be an object whose values are StringOrRef.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are StringOrRef."
severity: error
status: active
check: schema
---

`replaceElements` is `object (values: StringOrRef) or SIdRef`: the value, when not a reference, must be an object whose values are StringOrRef.
