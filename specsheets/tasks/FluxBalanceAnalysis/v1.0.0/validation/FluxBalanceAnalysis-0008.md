---
id: FluxBalanceAnalysis-0008
rule: The _type attribute of a FluxBalanceAnalysis must be "fluxBalanceAnalysis".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `FluxBalanceAnalysis` it must always equal `"fluxBalanceAnalysis"`.
