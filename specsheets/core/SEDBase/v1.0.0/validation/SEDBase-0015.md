---
id: SEDBase-0015
rule: "A reference required to resolve to a scalar value must apply enough non-range indices to reduce its target's shape to zero remaining dimensions."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' must resolve to a {expected-type}, but its target still has {count} dimension(s) remaining after indexing - only a non-range index removes a dimension, so a range anywhere in the chain leaves it in place."
severity: error
status: active
check: handwritten
---

This is the rule that actually backs every "must be a reference to a
number/string/..." field-level rule (see check: ref-type under Validation)
when the reference's target is a shaped AnnotatedData rather than a flat
constant. A range index (`[a:b]`) keeps its dimension in the result; a
positional or label index drops it (see Grammar). Resolving to a scalar
therefore requires every dimension to be eliminated by a positional or
label index, never a range. Applies uniformly to any scalar target type
(number, string, boolean, ...), not only numbers; the resolved scalar's
own type is then checked as usual by the field's own ref-type rule, not
by this one - this rule only covers the "still shaped" failure mode.
