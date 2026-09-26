---
id: CreateDataBlock-0004
rule: The _type attribute of a CreateDataBlock must be "createDataBlock".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `CreateDataBlock` it must always equal `"createDataBlock"`.
