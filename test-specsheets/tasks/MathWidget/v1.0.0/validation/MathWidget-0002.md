---
id: MathWidget-0002
rule: The math attribute of a MathWidget must be a string or a reference.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string or a reference."
severity: error
status: active
check: schema
---

`math` is `StringOrRef`; a literal must be a string. Whether the string is a well-formed expression is checked separately by `Types-0001` through `Types-0004`.
