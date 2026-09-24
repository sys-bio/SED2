---
id: ModelImport-0007
rule: The _type attribute of a ModelImport must be "modelImport".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `ModelImport` it must always equal `"modelImport"`.
