---
id: Curve-0002
rule: When the value of curveType of a Curve is provided directly, it must be one of 'points', 'bar', 'barStacked', 'horizontalBar', 'horizontalBarStacked', 'shadedArea'.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of {allowed}."
severity: error
status: active
---

`CurveType` is defined in `core/Types` with the allowed values 'points', 'bar', 'barStacked', 'horizontalBar', 'horizontalBarStacked', 'shadedArea' (see `core/Types/v1.0.0/schema.json`).
