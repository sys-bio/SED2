---
id: SimpleWidget-acme-0000
rule: The element fails a JSON Schema constraint attributable to the acme namespace's own additions to SimpleWidget that does not match any other numbered rule.
message: "{schema-message} (at {location})"
severity: error
status: active
---

Catch-all rule for schema-pass failures attributable specifically to the
acme namespace's own additions to SimpleWidget (currently just
acme@priority) - not to SimpleWidget's own base fields, which fall to
SimpleWidget-0000 instead. Rule ID follows the updated/ namespace scheme:
`<ClassName>-<prefix>-NNNN`.
