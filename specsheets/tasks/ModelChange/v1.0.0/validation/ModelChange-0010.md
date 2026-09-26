---
id: ModelChange-0010
rule: When the value of replaceElements of a ModelChange is a reference, it must be a reference to an object whose values are StringOrRef.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an object whose values are StringOrRef."
severity: error
status: active
check: ref-type
---

`replaceElements` is `object (values: StringOrRef) or SIdRef`: when the value is a reference, it must resolve to an object whose values are StringOrRef.
