# Annotation

![Annotation UML diagram](../../../core/SEDBase/v1.0.0/SEDBase.png)

*(`Annotation` has no standalone diagram of its own - the image above is `SEDBase`'s diagram, reused here because `Annotation` is drawn fully within it as a linked box, right next to `SEDBase`. Look for the `Annotation` box.)*

**Category:** auxiliary  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

A single qualifier/value pair attached to any `SEDBase`-derived element's `annotations` list, describing the parent object - e.g. `{"qualifier": "dc:license", "value": "http://creativecommons.org/publicdomain/zero/1.0/"}`. `qualifier` is a `"namespace:qualifier"` string (several namespaces are predefined for commonly-used modeling URIs, e.g. `bqbiol:hasPart`, `dc:title`, `bibo:Journal`); `value` may be any value (or a reference to one).

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `qualifier` | Qualifier | yes |  |
| `value` | AnyValueOrRef | yes |  |

### Attribute details

**`qualifier`** (Qualifier, required) - _(no description yet - placeholder, needs to be filled in)_

**`value`** (AnyValueOrRef, required) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Not independently referenceable - an `Annotation` only exists as an entry in its parent element's `annotations` list.

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

(Any output suffix not listed above is invalid for this class.)

Not independently referenceable - only exists as an entry in its parent element's `annotations` list.
