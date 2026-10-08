---
id: CellML-0003
rule: "When the model's language is CellML, a numerical index on its '.model' output is not valid."
message: "{class} '{id}' references '{value}', but CellML models cannot be indexed numerically."
severity: error
status: proposed
check: handwritten
---

CellML variables are identified by name only (see labels.md).  Labels
are the only supported form.
