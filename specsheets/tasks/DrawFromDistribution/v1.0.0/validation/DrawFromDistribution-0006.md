---
id: DrawFromDistribution-0006
rule: The _type attribute of a DrawFromDistribution must be "drawFromDistribution".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `DrawFromDistribution` it must always equal `"drawFromDistribution"`.
