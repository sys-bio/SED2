---
id: AbstractTask-0001
rule: The taskParameters attribute of an AbstractTask must be an array of TaskParameter objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of TaskParameter objects."
severity: error
status: active
check: schema
---

`taskParameters` is `array of TaskParameter` in AbstractTaskCommon: it must be an array of TaskParameter objects.
