---
id: Surface-0003
rule: When the value of surfaceType of a Surface is a reference, it must be a reference to a valid SurfaceType value.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a valid SurfaceType value."
severity: error
status: active
check: ref-type
---

`surfaceType` is `SurfaceType or SIdRef`: when the value is a reference, it must resolve to a valid SurfaceType value.
