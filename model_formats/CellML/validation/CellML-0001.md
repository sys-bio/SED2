---
id: CellML-0001
rule: "When the model's language is CellML, a label on its '.model' output must be the name of a variable of the top-level component."
message: "{class} '{id}' references '{value}', but the CellML model's top-level component has no variable named '{label}'."
severity: error
status: proposed
check: handwritten
---

Checked by a format-aware library only.  Without one, validation assumes the
label is potentially valid.
