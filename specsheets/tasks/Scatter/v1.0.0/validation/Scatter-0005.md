---
id: Scatter-0005
rule: The range attribute of a Scatter must be a RangeInline object.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a RangeInline object."
severity: error
status: active
check: schema
---

`range` must be a `Range`/`NumericRange`/`ParameterRange` object in its embedded `RangeInline` form.
