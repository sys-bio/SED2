---
id: ParameterScan-0007
rule: "The entries of a ParameterScan's parameterRanges must have pairwise distinct modelElement values."
message: "ParameterScan '{id}' has more than one entry in parameterRanges with modelElement '{value}'."
severity: error
status: active
check: handwritten
---

Stated in ParameterScan's description.md. Each ParameterRange scans one model
element, and its modelElement also labels its entry in [id].ranges and
[id].indexes, so two entries with the same modelElement would be both
ambiguous to address and redundant to scan. When modelElement is given as a
reference, entries are compared by the string it resolves to.
