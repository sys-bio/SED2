---
id: WidgetOptions-0002
rule: The timeoutSeconds attribute of a WidgetOptions-composing class, if present, must be a positive number.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive number."
severity: error
status: active
check: schema
---

`timeoutSeconds` is optional; when present, it must be a number > 0.
