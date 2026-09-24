---
id: Calculation-0004
rule: The _type attribute of a Calculation must be "calculation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `Calculation` it must always equal `"calculation"`.
