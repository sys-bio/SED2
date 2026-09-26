---
id: TestDocument-0002
rule: The widgets attribute of a TestDocument, if present, must be an object whose values are AbstractWidget objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractWidget objects."
severity: error
status: active
check: schema
---

`widgets` is optional; when present, each value must resolve to a concrete `AbstractWidget` branch.
