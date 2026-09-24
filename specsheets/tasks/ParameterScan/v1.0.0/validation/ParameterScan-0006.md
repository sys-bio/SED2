---
id: ParameterScan-0006
rule: The _type attribute of a ParameterScan must be "parameterScan".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `ParameterScan` it must always equal `"parameterScan"`.
