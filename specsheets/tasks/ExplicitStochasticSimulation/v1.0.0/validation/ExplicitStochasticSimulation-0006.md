---
id: ExplicitStochasticSimulation-0006
rule: The _type attribute of an ExplicitStochasticSimulation must be "explicitStochasticSimulation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `ExplicitStochasticSimulation` it must always equal `"explicitStochasticSimulation"`.
