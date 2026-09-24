# BoundedStochasticSimulation

![BoundedStochasticSimulation UML diagram](./BoundedStochasticSimulation.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"boundedStochasticSimulation"`  

## What it does

A stochastic simulation (see `ExplicitStochasticSimulation`) where only the start/end times are defined via the child `independentVariableSpan` (`Span`); between those points the simulator may output whenever it wishes - typically at every stochastic event, though `taskParameters` can control this if that would be too frequent.

This is an implementation of KISAO:0000319 (Monte Carlo method).

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md). `kisaoID`/`altDefinition` have been rolled into the `_type` discriminator and are no longer separate attributes.

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `model` | SIdRef | yes |  |
| `independentVariable` | StringOrRef | yes |  |
| `independentVariableInit` | NumberOrRef | no |  |
| `outputVariables` | ListOfStringsOrRef | yes |  |
| `workingAlgorithms` | array of WorkingAlgorithm | no |  |
| `independentVariableSpan` | SpanInline | yes |  |
| `seed` | NumberOrRef | no |  |
| `timeDependentRelativeTolerance` | NumberOrRef | no |  |
| `variableStepSize` | BooleanOrRef | no |  |
| `minimumTimeStep` | NumberOrRef | no |  |
| `maximumTimeStep` | NumberOrRef | no |  |
| `nonNegative` | BooleanOrRef | no |  |
| `maxOutputRows` | PositiveIntegerOrRef | no |  |
| `maxNumSteps` | PositiveIntegerOrRef | no |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`model`** (SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`independentVariable`** (StringOrRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`independentVariableInit`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`outputVariables`** (ListOfStringsOrRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`workingAlgorithms`** (array of WorkingAlgorithm, optional) - _(no description yet - placeholder, needs to be filled in)_

**`independentVariableSpan`** (SpanInline, required) - _(no description yet - placeholder, needs to be filled in)_

**`seed`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`timeDependentRelativeTolerance`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`variableStepSize`** (BooleanOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`minimumTimeStep`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`maximumTimeStep`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`nonNegative`** (BooleanOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`maxOutputRows`** (PositiveIntegerOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`maxNumSteps`** (PositiveIntegerOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

A 2D matrix of numbers, accessible as `[id]`, with solver-chosen row spacing. The model's end-of-run state is always also available as `[id].model`.

- `[id]`: **Valid**
    - Dimensions: 2D: columns = `independentVariable` plus one column per entry of `outputVariables`; row count is chosen by the simulator at run time (typically once per stochastic event) rather than fixed by `independentVariableSpan`.
- `[id].model`: **Valid**
- `[id].strings`: **Invalid**
