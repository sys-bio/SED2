---
id: TypesWidget-0002
rule: The _type attribute of a TypesWidget must be "typesWidget".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `TypesWidget` it must always equal `"typesWidget"`.
