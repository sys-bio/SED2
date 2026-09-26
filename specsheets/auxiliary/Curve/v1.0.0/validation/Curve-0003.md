---
id: Curve-0003
rule: When the value of curveType of a Curve is a reference, it must be a reference to a valid CurveType value.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a valid CurveType value."
severity: error
status: active
check: ref-type
---

`curveType` is `CurveType or SIdRef`: when the value is a reference, it must resolve to a valid CurveType value.
