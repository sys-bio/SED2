---
id: Report-0003
rule: The _type attribute of a Report must be "report".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `Report` it must always equal `"report"`.
