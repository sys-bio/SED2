---
id: SteadyState-0003
rule: The _type attribute of a SteadyState must be "steadyState".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `SteadyState` it must always equal `"steadyState"`.
