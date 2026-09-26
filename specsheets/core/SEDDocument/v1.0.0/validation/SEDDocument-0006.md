---
id: SEDDocument-0006
rule: The tasks attribute of a SEDDocument must be an object whose values are AbstractTask.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractTask."
severity: error
status: active
check: schema
---

`tasks` is `object (values: AbstractTask)`: it must be an object whose values are AbstractTask.
