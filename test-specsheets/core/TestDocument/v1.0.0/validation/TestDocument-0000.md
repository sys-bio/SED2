---
id: TestDocument-0000
rule: The element fails a JSON Schema constraint attributable to TestDocument that does not match any other numbered rule.
message: "{schema-message} (at {location})"
severity: error
status: active
check: schema
---

Catch-all rule for schema-pass failures attributable to TestDocument (or a
more specific descendant whose own class's failure location can't be
resolved to any other numbered rule). See Design.md, Schema-Pass Errors.
