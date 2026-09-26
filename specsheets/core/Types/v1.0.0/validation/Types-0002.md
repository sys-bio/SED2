---
id: Types-0002
rule: "Every function called in a math expression must be defined in the predefined-functions registry."
message: "The math in attribute '{attr}' of {class} '{id}' calls unknown function '{function}'."
severity: error
status: active
check: handwritten
---

The registry is schema/predefined-functions.json: the SBML L3 Core MathML
subset, the 12 distrib functions, and SED2's own additions (currently sum).
A namespace cannot add functions today; if that is wanted, the registry needs
a namespace extension point.
