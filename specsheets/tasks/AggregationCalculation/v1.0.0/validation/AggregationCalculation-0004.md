---
id: AggregationCalculation-0004
rule: The _type attribute of an AggregationCalculation must be "aggregationCalculation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `AggregationCalculation` it must always equal `"aggregationCalculation"`.
