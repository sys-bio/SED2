---
id: Range-0004
rule: A value that must resolve to a concrete Range subtype must declare a _type attribute.
message: "{location} must be a Range, but no _type at all was declared."
severity: error
status: active
check: schema
---

A narrower case of Range-0000's catch-all: fires specifically when
RangeInline's generated oneOf fails because _type is missing entirely,
rather than present but unrecognized. Wired via the x-missing-type-rule-id
keyword on RangeInline (inline.schema.json), a sibling of x-generated-oneOf;
see core-spec.md Section 8 and Design.md's Classes section.
