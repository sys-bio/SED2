---
id: ParameterRange-0016
rule: The _type attribute of a ParameterRange must be "parameterRange".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `ParameterRange` it must always equal `"parameterRange"`.
