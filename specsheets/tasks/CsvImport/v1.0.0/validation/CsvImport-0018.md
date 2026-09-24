---
id: CsvImport-0018
rule: The _type attribute of a CsvImport must be "csvImport".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `CsvImport` it must always equal `"csvImport"`.
