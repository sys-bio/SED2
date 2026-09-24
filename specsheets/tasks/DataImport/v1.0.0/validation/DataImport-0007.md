---
id: DataImport-0007
rule: The _type attribute of a DataImport must be "dataImport".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `DataImport` it must always equal `"dataImport"`.
