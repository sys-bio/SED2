---
id: CreateDataBlock-0002
rule: When the value of data of a CreateDataBlock is provided directly, it must be an object whose values are AnyValueOrRef.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AnyValueOrRef."
severity: error
status: active
check: schema
---

`data` is `object (values: AnyValueOrRef) or SIdRef`: the value, when not a reference, must be an object whose values are AnyValueOrRef.
