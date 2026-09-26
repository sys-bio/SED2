---
id: Surface-0002
rule: When the value of surfaceType of a Surface is provided directly, it must be one of 'parametricCurve', 'surfaceMesh', 'surfaceContour', 'contour', 'heatMap', 'stackedCurves', 'bar'.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of {allowed}."
severity: error
status: active
check: schema
---

`SurfaceType` is defined in `core/Types` with the allowed values 'parametricCurve', 'surfaceMesh', 'surfaceContour', 'contour', 'heatMap', 'stackedCurves', 'bar' (see `core/Types/v1.0.0/schema.json`).
