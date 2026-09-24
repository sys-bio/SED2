# AbstractReport

**Category:** outputs
**Schema:** [`schema.json`](./schema.json) + [`common.schema.json`](./common.schema.json) (`AbstractReportCommon`)

## What it does

Trimmed analog of `specsheets/outputs/AbstractOutput`: the `x-generated-oneOf` discriminator pattern on the outputs/ side of the tree, with one branch, `SimpleReport`. `AbstractReportCommon` contributes an optional `format`.

## Attributes

_This class defines no additional attributes beyond `TestBaseFields`; see `AbstractReportCommon` for what concrete branches inherit._
