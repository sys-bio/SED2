# AbstractWidget

**Category:** tasks
**Schema:** [`schema.json`](./schema.json) + [`common.schema.json`](./common.schema.json) (`AbstractWidgetCommon`)

## What it does

Trimmed analog of `specsheets/tasks/AbstractTask`: the `x-generated-oneOf` discriminator pattern, exercising the generator's discovery mechanism (see Design.md's Classes section) with two branches, `SimpleWidget` and `FancyWidget`. `common.schema.json`'s `AbstractWidgetCommon` contributes the fields every concrete widget inherits beyond `TestBase`: an optional `label`.

## Attributes

_This class defines no additional attributes beyond `TestBaseFields`; see `AbstractWidgetCommon` for what concrete branches inherit._
