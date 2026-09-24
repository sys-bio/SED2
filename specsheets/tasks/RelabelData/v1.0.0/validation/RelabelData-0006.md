---
id: RelabelData-0006
rule: The _type attribute of a RelabelData must be "relabelData".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `RelabelData` it must always equal `"relabelData"`.
