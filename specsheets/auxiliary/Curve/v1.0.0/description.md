# Curve

![Curve UML diagram](../../AbstractCurve/v1.0.0/AbstractCurve.png)

*(`Curve` has no standalone diagram of its own - the image above is `AbstractCurve`'s diagram, which already draws `Curve` directly as `AbstractCurve`'s one concrete subclass.)*

**Category:** auxiliary  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

`AbstractCurve` is the base class (see `auxiliary/AbstractCurve`); `Curve` is its only concrete subclass so far, always pinning `_type` to `"curve"` (a `ShadedArea` subclass, matching SED-ML, is expected to join it later - `AbstractCurve`'s `oneOf` is generated, so adding that branch needs no edit here). `Curve` composes `AbstractCurve`'s `AbstractCurveCommon` mixin - `x`, `order`, `style`, `yAxis` - and adds its own `curveType` (`"points"`, `"bar"`, `"barStacked"`, `"horizontalBar"`, `"horizontalBarStacked"`, or `"shadedArea"`), the `y` data reference, and the error-bar fields `xErrorLower`/`xErrorUpper`/`yErrorLower`/`yErrorUpper`. `yFrom`/`yTo` are meaningful only when `curveType` is `"shadedArea"`.

**One schema file in this folder.** `schema.json` defines `Curve` itself, composing `AbstractCurve`'s `AbstractCurveCommon` mixin (in `auxiliary/AbstractCurve/v1.0.0/common.schema.json`) via `allOf`, plus its own `_type`/`curveType`/`y`/error-bar/`yFrom`/`yTo` fields.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `_type` | const `"curve"` | yes |  |
| `curveType` | CurveType or SIdRef | yes |  |
| `x` | SIdRef | yes |  |
| `y` | SIdRef | yes |  |
| `order` | NonNegativeIntegerOrRef | no |  |
| `style` | SIdRef | no |  |
| `yAxis` | one of `"right"`, `"left"` or SIdRef | no |  |
| `xErrorUpper` | SIdRef | no |  |
| `xErrorLower` | SIdRef | no |  |
| `yErrorUpper` | SIdRef | no |  |
| `yErrorLower` | SIdRef | no |  |
| `yFrom` | SIdRef | no |  |
| `yTo` | SIdRef | no |  |

### Attribute details

**`_type`** (const `"curve"`, required) - The discriminator field; always `"curve"`.

**`curveType`** (CurveType or SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`x`** (SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`y`** (SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`order`** (NonNegativeIntegerOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`style`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yAxis`** (one of `"right"`, `"left"` or SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`xErrorUpper`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`xErrorLower`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yErrorUpper`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yErrorLower`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yFrom`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yTo`** (SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Not independently referenceable - a `Curve` only exists as a named child within a `Plot2D`'s `curves` dictionary.

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

(Any output suffix not listed above is invalid for this class.)

Not independently referenceable - only exists as a named child within a `Plot2D`'s `curves` dictionary.
