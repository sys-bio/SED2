# CreateDataBlock

![CreateDataBlock UML diagram](./CreateDataBlock.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"createDataBlock"`

## What it does

`CreateDataBlock` assembles a new block of `AnnotatedData` from several other pieces of data. Its `data` attribute is a dictionary mapping labels to values (numbers, lists, or `AnnotatedData`).

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `data` | object (values: AnyValueOrRef) or SIdRef | yes |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`data`** (object (values: AnyValueOrRef) or SIdRef, required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

A new `AnnotatedData` object whose labels are the `data` dictionary's keys and whose content is the corresponding values, accessible as `[id]`.

- `[id]`: **Valid**
    - Dimensions: dimension 0 has one entry per key in the `data` dictionary, labeled by those keys. If the values in `data` are themselves multi-dimensional (a list or `AnnotatedData`), their own dimensions follow dimension 0, so a block of vectors is a matrix: with a vector entry `r2`, `#tasks:blk['r2'][1]` (equivalently `#tasks:blk['r2', 1]`) is the second element of `r2`. All entries must have the same shape, since they are stacked into one array; entries of different shapes are an error when the document runs.
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**
