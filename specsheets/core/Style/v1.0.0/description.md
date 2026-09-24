# Style

*(No UML diagram exists yet for `Style` in the source spec - see [`DIAGRAM-PENDING.md`](./DIAGRAM-PENDING.md).)*

**Category:** core  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)

## What it does

`styles` is one of the four optional top-level dictionaries of a SED2 document, referenced from `Curve`/`Surface`/`Axis` children (via their `style` attribute) to control presentation.

**This class is not yet specified.** The current spec text says only: *"To be filled in; should be a straight copy of SED-ML's Style class."* The combined schema currently treats `Style` as a permissive placeholder (`{"type": "object"}`) accepting any object.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

_This class defines no additional attributes beyond `SEDBaseFields`._

## Outputs

- `[id]`: **Invalid**
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

(Any output suffix not listed above is invalid for this class.)

`Style` is an unspecified placeholder (see above) - how, or whether, a `Style` entry is referenced at all is not yet defined in the spec.

## Open issues / notes

- Style is a placeholder in both the prose spec and the schema. Once SED-ML's Style class is ported over, this Data Sheet (schema, diagram, and description) needs a full rewrite - flagging for your review rather than inventing a design here.
