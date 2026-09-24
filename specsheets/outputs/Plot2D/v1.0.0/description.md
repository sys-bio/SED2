# Plot2D

![Plot2D UML diagram](./Plot2D.png)

**Category:** outputs  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"plot2D"`

## What it does

A plot of two-dimensional data. Beyond `Plot`'s x/y axes, it adds an optional `rightYAxis` and a dictionary of named `curves` (each a `Curve`) to display.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `outputParameters` | array of OutputParameter | no |  |
| `legend` | BooleanOrRef | no |  |
| `height` | NumberOrRef | no |  |
| `width` | NumberOrRef | no |  |
| `xAxis` | Axis | no |  |
| `yAxis` | Axis | no |  |
| `rightYAxis` | Axis | no |  |
| `curves` | object (values: Curve) | yes |  |

### Attribute details

**`outputParameters`** (array of OutputParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`legend`** (BooleanOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`height`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`width`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`xAxis`** (Axis, optional) - _(no description yet - placeholder, needs to be filled in)_

**`yAxis`** (Axis, optional) - _(no description yet - placeholder, needs to be filled in)_

**`rightYAxis`** (Axis, optional) - _(no description yet - placeholder, needs to be filled in)_

**`curves`** (object (values: Curve), required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

By design, nothing further - as an `AbstractOutput`, a `Plot2D` is a terminal node.

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

(Any output suffix not listed above is invalid for this class.)

Terminal node - see `AbstractOutput`.
