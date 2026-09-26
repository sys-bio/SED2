---
id: SEDDocument-0007
rule: The outputs attribute of a SEDDocument must be an object whose values are AbstractOutput.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractOutput."
severity: error
status: active
check: schema
---

`outputs` is `object (values: AbstractOutput)`: it must be an object whose values are AbstractOutput.
