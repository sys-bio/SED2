---
id: ExplicitODESimulation-0006
rule: The _type attribute of an ExplicitODESimulation must be "explicitODESimulation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `ExplicitODESimulation` it must always equal `"explicitODESimulation"`.
