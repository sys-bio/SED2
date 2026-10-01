# FluxBalanceAnalysis

![FluxBalanceAnalysis UML diagram](./FluxBalanceAnalysis.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"fluxBalanceAnalysis"`

## What it does

Uses an objective function and reaction rate bounds (both defined within the model itself) to determine the set of reaction rates that maximizes the objective function. Unlike the other simulation tasks, FBA has no independent variable.

This is an implementation of KISAO:0000437 (FBA). The algorithm(s) it uses internally may be listed in the optional `workingAlgorithms` (see `WorkingAlgorithm`).

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `model` | SIdRef | yes |  |
| `outputVariables` | ListOfStringsOrRef | yes |  |
| `workingAlgorithms` | array of WorkingAlgorithm | no |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`model`** (SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`outputVariables`** (ListOfStringsOrRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`workingAlgorithms`** (array of WorkingAlgorithm, optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

A dictionary of model variables (usually fluxes) to their final values, accessible via `outputVariables` as `[id]` - analogous to a `SteadyState` result. The resulting model state is always also available as `[id].model`.

- `[id]`: **Valid**
    - Dimensions: 1D: one value per entry of `outputVariables` (typically reaction fluxes) - length depends on how many variables are named there.
- `[id].model`: **Valid**
- `[id].strings`: **Invalid**
