---
id: BoundedODESimulation-0006
rule: The _type attribute of a BoundedODESimulation must be "boundedODESimulation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `BoundedODESimulation` it must always equal `"boundedODESimulation"`.
