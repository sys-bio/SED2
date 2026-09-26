---
id: SEDDocument-0010
rule: "A <prefix>@version attribute should not be declared for a namespace the document never uses."
message: "The document declares '{attr}', but namespace '{prefix}' is not used anywhere."
severity: warning
status: active
check: handwritten
---

Harmless but likely a leftover.
