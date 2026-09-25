---
id: AbstractWidget-0002
rule: A value that must resolve to a concrete AbstractWidget subtype must declare a _type attribute.
message: "{location} must be an AbstractWidget, but no _type at all was declared."
severity: error
status: active
---

A narrower case of AbstractWidget-0000's catch-all: fires specifically when
the generated oneOf fails because _type is missing entirely, rather than
present but unrecognized. Wired via the x-missing-type-rule-id keyword,
a sibling of x-generated-oneOf; see core-spec.md Section 8 and Design.md's
Classes section.
