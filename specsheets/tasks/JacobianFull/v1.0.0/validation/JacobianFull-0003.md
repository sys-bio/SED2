---
id: JacobianFull-0003
rule: The _type attribute of a JacobianFull must be "jacobianFull".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `JacobianFull` it must always equal `"jacobianFull"`.
