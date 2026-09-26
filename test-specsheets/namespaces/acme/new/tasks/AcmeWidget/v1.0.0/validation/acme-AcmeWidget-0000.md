---
id: acme-AcmeWidget-0000
rule: The element fails a JSON Schema constraint attributable to acme@AcmeWidget that does not match any other numbered rule.
message: "{schema-message} (at {location})"
severity: error
status: active
check: schema
---

Catch-all rule for schema-pass failures attributable to acme@AcmeWidget (or a
more specific descendant whose own class's failure location can't be
resolved to any other numbered rule). See Design.md, Schema-Pass Errors.
Rule ID follows the new/ namespace scheme: `<prefix>-<ClassName>-NNNN`.
