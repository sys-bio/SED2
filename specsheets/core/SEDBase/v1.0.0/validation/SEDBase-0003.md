---
id: SEDBase-0003
rule: The notes attribute of a SEDBase-derived element, if present, must be a markdown-formatted string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a markdown-formatted string."
severity: error
status: active
---

`notes` is a `MarkdownString` in SEDBaseFields - a CommonMark-formatted string.
