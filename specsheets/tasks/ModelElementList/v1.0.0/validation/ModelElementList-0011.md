---
id: ModelElementList-0011
rule: The _type attribute of a ModelElementList must be "modelElementList".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `ModelElementList` it must always equal `"modelElementList"`.
