---
id: WeightedChoice-0002
rule: The _type attribute of a WeightedChoice must be "weightedChoice".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `WeightedChoice` it must always equal `"weightedChoice"`.
