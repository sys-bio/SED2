---
id: AggregationCalculation-0002
rule: When the value of appliedDimensions of an AggregationCalculation is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
check: schema
---

`appliedDimensions` is `ListOfStringsOrRef`: the value, when not a reference, must be an array of strings.
