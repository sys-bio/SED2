---
id: WidgetOptions-0001
rule: The retries attribute of a WidgetOptions-composing class, if present, must be a non-negative integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a non-negative integer."
severity: error
status: active
check: schema
---

`retries` is optional; when present, it must be an integer >= 0.
