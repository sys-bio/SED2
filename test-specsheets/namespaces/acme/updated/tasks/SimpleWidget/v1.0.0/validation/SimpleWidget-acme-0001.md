---
id: SimpleWidget-acme-0001
rule: If present, the acme@priority attribute of a SimpleWidget must be non-negative.
message: "Attribute '{attr}' of {class} '{id}' must be >= 0."
severity: error
status: active
---

`acme@priority` is optional, but when present must resolve to a non-negative number. Rule ID follows the updated/ namespace scheme: `<ClassName>-<prefix>-NNNN`.
