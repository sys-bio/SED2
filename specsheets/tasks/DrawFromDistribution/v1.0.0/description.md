# DrawFromDistribution

![DrawFromDistribution UML diagram](./DrawFromDistribution.png)

**Category:** tasks  
**Version:** v1  
**Schema:** [`schema.json`](./schema.json)  
**`_type` discriminator:** `"drawFromDistribution"`

## What it does

Draws from one of the distributions defined in the SBML specification: normal, cauchy, chisquare, exponential, gamma, laplace, lognormal, rayleigh, binomial, and poisson - previously named via `altDefinition` (see note below). `arguments` supplies the distribution's parameters in the order SBML defines them - e.g. a normal distribution takes `(mean, stdev)` or `(mean, stdev, min, max)`. For distributions outside the SBML list, other ontologies (e.g. UncertML, though dormant) may be used.

`outputPersistent` controls whether every reference to this task's id always yields the same drawn value (`true` - useful when multiple tasks must share one draw) or yields a fresh draw from the same distribution each time it's referenced (`false` - useful when multiple tasks need independent draws).

## Attributes

All classes additionally inherit the optional `name`, `description`, `notes`, and `annotations` fields from `SEDBase` - see [`core/SEDBase`](../../../core/SEDBase/v1.0.0/description.md). `kisaoID`/`altDefinition` have been rolled into the `_type` discriminator and are no longer separate attributes.

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `taskParameters` | array of TaskParameter | no |  |
| `arguments` | ListOfAnyOrRef | yes |  |
| `outputPersistent` | BooleanOrRef | no |  |

### Attribute details

**`taskParameters`** (array of TaskParameter, optional) - _(no description yet - placeholder, needs to be filled in)_

**`arguments`** (ListOfAnyOrRef, required) - _(no description yet - placeholder, needs to be filled in)_

**`outputPersistent`** (BooleanOrRef, optional) - _(no description yet - placeholder, needs to be filled in)_


## Outputs

Officially `AnnotatedData`, usually a single number accessible as `[id][0]`; the type is multidimensional to leave room for future draws of correlated values.

- `[id]`: **Valid**
    - Dimensions: Currently always a single value, at `[id][0]` (effectively 0-D/scalar today). _(How a future correlated multi-value draw would be shaped is open - placeholder.)_
- `[id].model`: **Invalid**
- `[id].strings`: **Invalid**

Typically a single number, indexed as `[id][0]`; the type is multidimensional `AnnotatedData` to leave room for correlated multi-value draws in the future.

## Open issues / notes

- `kisaoID`/`altDefinition` have been rolled into the `_type` discriminator rather than being separate attributes - it's not yet clear from the docs alone how the distribution is now named without `altDefinition`.
