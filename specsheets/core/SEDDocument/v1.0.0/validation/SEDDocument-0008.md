---
id: SEDDocument-0008
rule: The styles attribute of a SEDDocument must be an object whose values are Style.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are Style."
severity: error
status: active
check: schema
---

`styles` is `object (values: Style)`: it must be an object whose values are Style.
