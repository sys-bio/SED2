# Repeat

![Repeat UML diagram](./Repeat.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

Like SED-ML Level 1's RepeatedTask, SED2 needs to repeat a group of tasks multiple times. `Repeat` is the set of fields shared by all three concrete subclasses (`Scatter`, `Loop`, `ParameterScan`), composed via `allOf` rather than instantiated on its own - the prose spec calls this abstract concept simply "Repeat".

The repeat's `subTasks` are true children (not references) of the parent, and may depend on each other, on outputs of tasks outside the repeat, or on the repeat's own per-iteration outputs (the current iteration's range value and position: `[id].range`/`[id].index` for `Scatter` and `Loop`, `[id].ranges`/`[id].indexes` for `ParameterScan` - see those classes). `outputVariableMap` (optional) defines the entries of the repeat's own `[id]` output: each named entry maps an output name to a value produced by a subTask, and the names label that dimension. For `Scatter` and `Loop`, dimension 0 of `[id]` is the iteration (labeled by the range values) and dimension 1 holds the `outputVariableMap` entries; for `ParameterScan` there is one dimension per parameter range, followed by the `outputVariableMap` entries; see each subclass for its exact `[id]` shape. All entries of one `outputVariableMap` must have the same shape, since they are stacked into one array. `aggregateOutputVariables` defines the columns of `[id].aggregates` - used to efficiently collect running summary statistics (e.g. mean/stdev) across a very large number of repeats without keeping every individual run's output; entries here may not define their own `appliedDimensions` (the applied dimension is always 'the Repeat' itself), and each `input` must reference a subTask's output.

A `Repeat`-derived task must define at least one of `outputVariableMap` or `aggregateOutputVariables`.

`Repeat` itself has no `range`: `Loop` and `Scatter` each define their own required `range` child (a `Range`/`NumericRange`/`ParameterRange`), and `ParameterScan` uses `parameterRanges` instead.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `subTasks` | object (values: AbstractTask) | no |  |
| `outputVariableMap` | object (values: SIdRef) or SIdRef | no | Optional, but at least one of this or `aggregateOutputVariables` must be provided (Repeat-0006). |
| `aggregateOutputVariables` | object (values: AggregationCalculation) | no |  |

### Attribute details

**`subTasks`** (object (values: AbstractTask), optional) - _(no description yet - placeholder, needs to be filled in)_

**`outputVariableMap`** (object (values: SIdRef) or SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`aggregateOutputVariables`** (object (values: AggregationCalculation), optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Not applicable on its own - see `Scatter`, `Loop`, and `ParameterScan` for their concrete output shapes (`[id]` per `outputVariableMap`, `[id].aggregates` per `aggregateOutputVariables`). The per-iteration range outputs (`[id].range`/`[id].index` on `Scatter` and `Loop`, `[id].ranges`/`[id].indexes` on `ParameterScan`) belong to those subclasses, not to `Repeat`.

Shared mixin for the three `Repeat` subclasses - not instantiated on its own; see `Scatter`, `Loop`, `ParameterScan`.
