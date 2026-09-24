---
id: CreateDataBlock-0003
rule: When the value of data of a CreateDataBlock is a reference, it must be a reference to an object whose values are AnyValueOrRef.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an object whose values are AnyValueOrRef."
severity: error
status: active
---

`data` is `object (values: AnyValueOrRef) or SIdRef`: when the value is a reference, it must resolve to an object whose values are AnyValueOrRef.
