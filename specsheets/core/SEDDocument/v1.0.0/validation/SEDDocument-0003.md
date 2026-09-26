---
id: SEDDocument-0003
rule: The version attribute of a SEDDocument must match the format v#.#.# (major.minor.patch).
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required format 'v#.#.#'."
severity: error
status: active
check: schema
---

`version` must match the pattern `v#.#.#` (e.g. `v1.0.0`).
