---
id: SEDBase-0004
rule: The annotations attribute of a SEDBase-derived element, if present, must be an array of Annotation objects.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of Annotation objects."
severity: error
status: active
---

`annotations` is an array of `Annotation` objects in SEDBaseFields, each with a required `qualifier` (a `Qualifier` string, e.g. 'bqbiol:hasPart') and a required `value` (`AnyValueOrRef`).
