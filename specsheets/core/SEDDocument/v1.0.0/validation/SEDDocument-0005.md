---
id: SEDDocument-0005
rule: The constants attribute of a SEDDocument must be an object whose values are AnyValueOrRef.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AnyValueOrRef."
severity: error
status: active
check: schema
---

`constants` is `object (values: AnyValueOrRef)`: it must be an object whose values are AnyValueOrRef.
