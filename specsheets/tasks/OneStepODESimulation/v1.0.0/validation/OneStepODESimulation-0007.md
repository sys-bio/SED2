---
id: OneStepODESimulation-0007
rule: The _type attribute of an OneStepODESimulation must be "oneStepODE".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `OneStepODESimulation` it must always equal `"oneStepODE"`.
