---
id: CellML-0002
rule: "When the model's language is CellML, a label on its '.model' output must not name a variable that exists only in a subcomponent."
message: "{class} '{id}' references '{value}', but '{label}' is a variable of a subcomponent, which is not accessible."
severity: error
status: proposed
check: handwritten
---

Elements of subcomponents are officially inaccessible in CellML (see
labels.md).  If the top-level component has a variable of the same name,
the label names that variable and this rule does not fire.
