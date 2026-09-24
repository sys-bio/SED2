---
id: OutputParameter-0001
rule: The value attribute of an OutputParameter is required.
message: "Required attribute '{attr}' is missing from {class} '{id}'."
severity: error
status: active
---

`value` is required. Its type is `AnyValueOrRef` - any JSON value or a reference is accepted, so no separate type rule applies beyond presence.
