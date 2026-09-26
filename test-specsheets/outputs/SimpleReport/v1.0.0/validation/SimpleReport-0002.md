---
id: SimpleReport-0002
rule: The _type attribute of a SimpleReport must be "simpleReport".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `SimpleReport` it must always equal `"simpleReport"`.
