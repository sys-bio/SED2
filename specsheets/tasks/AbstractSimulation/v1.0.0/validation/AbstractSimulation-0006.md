---
id: AbstractSimulation-0006
rule: When the value of outputVariables of an AbstractSimulation is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
check: schema
---

`outputVariables` is `ListOfStringsOrRef` in AbstractSimulation: the value, when not a reference, must be an array of strings.
