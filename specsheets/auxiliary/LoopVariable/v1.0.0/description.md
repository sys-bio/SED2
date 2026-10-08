# LoopVariable

![LoopVariable UML diagram](./LoopVariable.png)

**Category:** auxiliary  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

A named child of a `Loop`, representing a value that starts at `initialValue` (sometimes called a 'seed' in workflow languages) on the loop's first iteration, and thereafter takes on `subsequentValues` - a reference to an output of one of the loop's `subTasks`. A subTask reads the current value as `#tasks:[loop_id]:loopVariables:[loopvar_id]`.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `initialValue` | AnyValueOrRef | yes |  |
| `subsequentValues` | SIdRef | yes |  |

### Attribute details

**`initialValue`** (AnyValueOrRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`subsequentValues`** (SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Not independently referenceable outside its parent `Loop` - see `Loop` for how its current value is addressed from a subTask.

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

Additional possible outputs beyond the three standard ones:

- `#tasks:[loop_id]:loopVariables:[loopvar_id]`: A `LoopVariable`'s current value, addressed this way from within a subTask - not via the `[id]`/`[id].model`/`[id].strings` scheme, since a `LoopVariable` is not itself a `tasks` dictionary entry.
    - Dimensions: The same as `initialValue` itself: the value at the current iteration (`initialValue` on the first, then `subsequentValues` from the previous one), not one value per iteration. (`initialValue` is typed `anyType` in the schema, so its own shape is otherwise open/unconstrained.)

Not independently referenceable outside its parent `Loop`.
