# MathWidget

**Category:** tasks
**Schema:** [`schema.json`](./schema.json)

## What it does

Leaf branch of `AbstractWidget` (`_type` "mathWidget"), flatly composing `TestBaseFields` + `AbstractWidgetCommon`. Trimmed analog of `specsheets/tasks/Calculation`: one required `math` attribute holding an infix expression. Exercises the `x-math` marker on a `StringOrRef` field, which makes the generated `validate()` run the shared math-grammar rules (`core/Types` `Types-0001` through `Types-0004`) on a literal value.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `math` | StringOrRef (`x-math`) | yes | infix expression; a reference is not parsed |
