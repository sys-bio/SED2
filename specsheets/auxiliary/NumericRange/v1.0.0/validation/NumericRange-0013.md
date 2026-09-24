---
id: NumericRange-0013
rule: The _type attribute of a NumericRange must be "numericRange".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `NumericRange` it must always equal `"numericRange"`.
