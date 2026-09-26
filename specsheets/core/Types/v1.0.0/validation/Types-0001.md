---
id: Types-0001
rule: "A math expression must be a well-formed expression under the SED2 infix grammar."
message: "The math in attribute '{attr}' of {class} '{id}' could not be parsed: '{expr}'. {parse-message}"
severity: error
status: active
check: handwritten
---

The grammar is the one in Design.md's Math section (math.g4). {parse-message}
is the parser's own error text. When the math attribute is itself a
reference, this and the following math rules (Types-0002 through Types-0004)
apply only if the reference resolves statically to a string constant.

Lives on Types, alongside StringOrRef (the schema type every math-bearing
attribute uses), rather than on Calculation: Calculation's math is the only
field that uses these rules today, but Design.md's Classes section notes
that may not stay true, and a shared home avoids either duplicating these
four rules per class or attaching Calculation-specific numbering to a
generic grammar concern.
