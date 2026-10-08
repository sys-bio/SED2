# Scatter

![Scatter UML diagram](./Scatter.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"scatter"`

## What it does

A `Repeat` whose iterations are guaranteed fully independent of one another - no subTask output from one iteration feeds into another - so a conforming interpreter may execute the iterations in parallel if it chooses. `range` (a required `Range`/`NumericRange`/`ParameterRange` child) defines one iteration per element.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `subTasks` | object (values: AbstractTask) | yes |  |
| `outputVariableMap` | object (values: SIdRef) or SIdRef | no |  |
| `aggregateOutputVariables` | object (values: AggregationCalculation) | no |  |
| `range` | RangeInline | yes |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`subTasks`** (object (values: AbstractTask), required) - _(no description yet - placeholder, needs to be filled in)_

**`outputVariableMap`** (object (values: SIdRef) or SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`aggregateOutputVariables`** (object (values: AggregationCalculation), optional) - _(no description yet - placeholder, needs to be filled in)_

**`range`** (RangeInline, required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

`[id]`: an `AnnotatedData` with one row per iteration (dimension 0, labeled by the range values) and one entry per `outputVariableMap` key (dimension 1, labeled by the keys); the range values themselves are not a column. `[id].aggregates`: an `AnnotatedData` following `aggregateOutputVariables`, when defined.

- `[id]`: **Valid**
    - Dimensions: 2D (or more). Dimension 0 is the iteration: one row per value in `range`, labeled by those values. Dimension 1 holds the `outputVariableMap` entries, one per key, labeled by the keys (length 0 if `outputVariableMap` is empty). If an entry's own value is not a scalar, its dimensions (with their labels) follow, so a scalar-valued map gives a plain iterations-by-entries table. All entries must have the same shape, since they are stacked into one array; entries of different shapes are an error when the document runs. Labels are text: the range values are written the way numbers appear in formed strings (see `StringFormation`): an integral value without a decimal point (`1`, not `1.0`), otherwise as the shortest decimal that reads back as the same number (`0.5`, `0.25`).
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

Additional possible outputs beyond the three standard ones:

- `[id].aggregates`: An `AnnotatedData` following `aggregateOutputVariables`, when that attribute is defined.
    - Dimensions: 1D: one entry per `aggregateOutputVariables` mapping. Each entry's aggregation function collapses the `range` dimension of `[id]` (per `Repeat`, the applied dimension defaults to 'the Repeat' itself, i.e. this one) down to a single value - unless the underlying subTask output was itself multi-dimensional, in which case that dimensionality carries through per entry (further dimensions follow the first).

- `[id].range`: Within each iteration, the current value of `range`. Always valid, since `range` is required.
    - Dimensions: Scalar (0-D) per iteration.
- `[id].index`: Within each iteration, the current index into `range`. Always valid.
    - Dimensions: Scalar (0-D) per iteration.
