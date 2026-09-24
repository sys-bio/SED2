---
id: OneStepStochasticSimulation-0006
rule: The _type attribute of an OneStepStochasticSimulation must be "oneStepStochastic".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `OneStepStochasticSimulation` it must always equal `"oneStepStochastic"`.
