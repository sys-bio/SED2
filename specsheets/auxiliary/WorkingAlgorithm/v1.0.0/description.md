# WorkingAlgorithm

![WorkingAlgorithm UML diagram](../../../tasks/AbstractSimulation/v1.0.0/AbstractSimulation.png)

*(`WorkingAlgorithm` has no standalone diagram of its own - the image above is `AbstractSimulation`'s diagram, reused here because `WorkingAlgorithm` is drawn fully within it as a linked box, right next to `AbstractSimulation`. Look for the `workingAlgorithm` box.)*

**Category:** auxiliary  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  

## What it does

An algorithm used internally by a simulation task, attached via `AbstractSimulation`'s `workingAlgorithms` list. Beyond the fields it inherits from `SEDBase`, it carries a required `algorithm`.

_(No description yet - placeholder. It's not yet clear from the diagram alone how `algorithm` relates to the task's own `_type` discriminator and `taskParameters`, or how multiple `workingAlgorithms` entries on one task are meant to be distinguished/used - needs updating once that's settled.)_

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `algorithm` | StringOrRef | yes |  |

### Attribute details

**`algorithm`** (StringOrRef, required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Not independently referenceable - a `WorkingAlgorithm` only exists as an entry in its parent simulation task's `workingAlgorithms` list.

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

(Any output suffix not listed above is invalid for this class.)

Not independently referenceable - only exists as an entry in its parent task's `workingAlgorithms` list.
