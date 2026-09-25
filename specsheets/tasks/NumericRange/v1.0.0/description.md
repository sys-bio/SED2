# NumericRange

![NumericRange UML diagram](../../Range/v1.0.0/Range.png)

*(`NumericRange` has no standalone diagram of its own - the image above is `Range`'s diagram; `NumericRange` inherits directly from `Range` and adds nothing that would need separate illustration.)*

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json) + [`inline.schema.json`](./inline.schema.json) (`NumericRangeInline`)  
**`_type` discriminator:** `"numericRange"`

## What it does

A restricted `Range` (its subclass) whose values are numeric, definable several ways. Explicitly listing every value in `values` (in which case no other attribute may be set) is one option. The other five options each use a subset of `start`, `end`, `numberOfSteps`, and `interval`:

- **`numberOfSteps` alone**: a range from 0 to `numberOfSteps` with an interval of 1.
- **`start`, `end`, `numberOfSteps` (+ required `scale`)**: the start-end interval is divided into `numberOfSteps` equal sub-intervals on a `"linear"` or `"log10"` scale, with data collected at the start and end of each sub-interval. `scale` may only (and must) be set for this combination.
- **`start`, `numberOfSteps`, `interval`**: `numberOfSteps` points collected every `interval` after `start`, with an implied end.
- **`end`, `numberOfSteps`, `interval`**: `numberOfSteps` points collected every `interval` up to `end`, with an implied start.
- **`start`, `interval`, `end`**: points collected every `interval` past `start` until `end` is reached; `end` is always included as the final point even when it doesn't fall exactly on an interval boundary. Whether a separately-calculated near-`end` point is *also* included depends on a tolerance of `interval * 1e-6`: if the nearest calculated point is within that tolerance of `end`, only `end` is kept; otherwise both are kept. For example, `start=0, end=10, interval=3` yields `[0, 3, 6, 9, 10]`; `start=0, end=10, interval=3.333` yields `[0, 3.333, 6.666, 9.999, 10]` (9.999 is far enough from 10); `interval=3.333333` instead yields `[0, 3.333333, 6.666666, 10]` (9.999999 is within tolerance of 10, so it's dropped in favor of the exact endpoint).

The spec explicitly warns that relying on readers to work out this tolerance to know what values a range produces is not best practice - output end times should generally be a simple multiple of the interval, plus the start.

**Three schema files in this folder.** `schema.json` defines `NumericRange` itself (usable standalone, as a `tasks` dictionary entry), composing `Range`'s `RangeCommon` mixin alongside its own `NumericRangeCommon`. `common.schema.json` defines `NumericRangeCommon` - `start`/`end`/`interval`/`numberOfSteps`/`scale` plus `values` narrowed to numeric-only - composed via `allOf` by `NumericRange` itself and, in turn, by `ParameterRange`. `inline.schema.json` defines `NumericRangeInline` - the wrapper used for named child fields that must be specifically numeric, e.g. `ExplicitODESimulation.independentVariableRange` / `ExplicitStochasticSimulation.independentVariableRange`. See `tasks/Range` for why the standalone and common forms are kept separate.

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md).

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `start` | NumberOrRef | no |  |
| `end` | NumberOrRef | no |  |
| `interval` | PositiveDoubleOrRef | no |  |
| `numberOfSteps` | PositiveIntegerOrRef | no |  |
| `scale` | ScaleTypeOrRef | no |  |
| `values` | array of NumberOrRef or SIdRef | no |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`start`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`end`** (NumberOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`interval`** (PositiveDoubleOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`numberOfSteps`** (PositiveIntegerOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`scale`** (ScaleTypeOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_

**`values`** (array of NumberOrRef or SIdRef, optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

When used as a named child (e.g. `independentVariableRange`, `independentVariableSpan`'s sibling forms), `NumericRange` has no independent output - its values are consumed directly by the containing task. When it appears directly in the `tasks` dictionary, its output is the list of numeric values, accessible as `[id]`.

- `[id]`: **Valid**
    - Dimensions: 1D: one value per generated point - either `len(values)` if given explicitly, or `numberOfSteps` (+1, since both endpoints are included) when generated from `start`/`end`/`interval`/`scale`.
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

Only valid when `NumericRange` is used directly as a `tasks` dictionary entry. As an embedded child (via `NumericRangeInline`), it has no independent output of its own.
