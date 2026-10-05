---
id: FluxBalanceAnalysis-0009
rule: The workingAlgorithms attribute of a FluxBalanceAnalysis, if present, must be an array of WorkingAlgorithm objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of WorkingAlgorithm objects."
severity: error
status: active
check: schema
---

`workingAlgorithms` is optional; when present, each entry must be a `WorkingAlgorithm` object.
