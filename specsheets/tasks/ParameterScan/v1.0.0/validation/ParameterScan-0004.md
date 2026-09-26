---
id: ParameterScan-0004
rule: The parameterRanges attribute of a ParameterScan must be an array of ParameterRangeInline objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of ParameterRangeInline objects."
severity: error
status: active
check: schema
---

`parameterRanges` is `array of ParameterRangeInline`: it must be an array of ParameterRangeInline objects.
