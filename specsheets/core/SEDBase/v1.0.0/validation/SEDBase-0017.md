---
id: SEDBase-0017
rule: "A reference required to resolve to AnnotatedData must resolve to AnnotatedData."
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to {resolved-value}, not AnnotatedData."
severity: error
status: active
check: handwritten
---

Applies to every field whose schema property carries
`"x-ref-target": "annotatedData"` (AbstractCurve's `x`; Curve's `y`, `xErrorUpper`,
`xErrorLower`, `yErrorUpper`, `yErrorLower`, `yFrom` and `yTo`; Surface's `x`, `y`
and `z`; RelabelData's `input`; Report's `data`).

AnnotatedData is an n-dimensional block of values, labeled or not, and a bare
scalar is the 0-dimensional case. A reference resolves to it when it names (a) a
constant whose value is a number, string, boolean or array (an unlabeled
AnnotatedData), or (b) a task output whose outputs.json entry has "type":
"annotatedData" or "stringList". A model is not AnnotatedData, and neither is an
object constant.

A reference that does not resolve at all (SEDBase-0006), targets an output
(SEDBase-0007), or uses an accessor its target does not declare (SEDBase-0008)
fires those rules instead of this one.
