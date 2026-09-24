# Curve

![Curve UML diagram](./Curve.png)

**Category:** auxiliary  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

The prose spec calls this class `AbstractCurve`; because it currently has only one concrete form, the schema names the concrete, directly-usable class `Curve` (no `_type` discriminator is needed). It defines a single 2D curve within a `Plot2D`'s `curves` dictionary: `curveType` (`"points"`, `"bar"`, `"barStacked"`, `"horizontalBar"`, `"horizontalBarStacked"`, or `"shadedArea"`), the `x`/`y` data references, an optional `order`, `style` reference, and which `yAxis` (`"left"` or `"right"`) it plots against. Error-bar fields `xErrorLower`/`xErrorUpper`/`yErrorLower`/`yErrorUpper` are also available. `yFrom`/`yTo` are meaningful only when `curveType` is `"shadedArea"`.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md). `kisaoID`/`altDefinition` have been rolled into the `_type` discriminator and are no longer separate attributes.

| Attribute | Type | Required | Notes |
|---|---|---|---|
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
