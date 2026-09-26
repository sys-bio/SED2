---
id: JacobianReduced-0003
rule: The _type attribute of a JacobianReduced must be "jacobianReduced".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `JacobianReduced` it must always equal `"jacobianReduced"`.
