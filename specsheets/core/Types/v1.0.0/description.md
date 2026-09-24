# Types

*(This page bundles the shared primitive and reference-helper types; it has no single UML class box of its own - see `core/SEDBase` for the base class every element derives from.)*

**Category:** core  
**Schema:** [`schema.json`](./schema.json)

## What this covers

Every value in a SED2 document is either a literal value or a *reference* to a value elsewhere in the document. Anywhere the spec calls for, say, a `double`, that slot may instead hold a string reference such as `"#tasks:sim1.model['S1']"` that resolves to a double at read time. This page collects the primitive and reference-helper types used throughout the rest of the spec; it has no UML class of its own.

**Base value kinds.** Numbers (integers, doubles, etc.), Booleans, Strings, AnnotatedData (n-dimensional matrices of values with labeled coordinates and dimensions, modeled after `xarray.DataArray`), Models (a set of values/state plus the rules for how those values change), and Maps (a 1:1 mapping of one type to another, e.g. `{SId: SIdRef}`).

**Special number rules.** The strings `"nan"`, `"inf"`, and `"-inf"` (any capitalization) represent NaN, +Infinity and -Infinity respectively when found among numbers; a mix of strings and numbers in the same 1D AnnotatedData is an error unless every string is one of these three. Booleans may be parsed numerically as 1 or 0.

**References.** A reference is a `#`-prefixed, colon-delimited path following the document's hierarchical structure (e.g. `#tasks:sim1`, `#tasks:sim1.loc[0]`, `#tasks:sim1.model["S1"]`, `#tasks:data_import["S1"].loc[3]`, `#constants:time_end`). A task's own id always has an implicit `.model` accessor when it exports a model, and a `.strings` accessor when it exports a list of strings. AnnotatedData supports positional indexing (`data[0, :]`), `.loc` (positional + coordinate label), `.isel` (dimension name + integer label), and `.sel` (dimension name + coordinate label), following the equivalent xarray/pandas/numpy conventions.

## Attributes

Not attributes of a class - `Types` instead bundles the following primitive/reference-helper `$defs`, each usable via `$ref` from any other Data Sheet's schema:

| Name | Description |
|---|---|
| `SId` | An identifier: starts with an English letter or underscore, may be followed by alphanumerics or underscores. |
| `SIdRef` | A reference to another SED element. Always starts with '#'. May include a colon-delimited path, dot-accessors (e.g. .model, .strings, .aggregates), and indexing ([n], [-n], ['label'], [a:b]). |
| `KISAOId` | A KiSAO identifier of the form KISAO:nnnnnnn (7 digits). |
| `URI` | A URI string. Can be absolute or relative. |
| `URN` | A URN string. |
| `MarkdownString` | A CommonMark-formatted markdown string. |
| `NumberWithNaN` | A number, Boolean, or one of the special strings nan / inf / -inf (case-insensitive), which represent NaN, +Infinity, and -Infinity respectively. |
| `ScaleType` | One of `"linear"` or `"log10"`. |
| `CurveType` | One of `"points"`, `"bar"`, `"barStacked"`, `"horizontalBar"`, `"horizontalBarStacked"`, or `"shadedArea"`. |
| `SurfaceType` | One of `"parametricCurve"`, `"surfaceMesh"`, `"surfaceContour"`, `"contour"`, `"heatMap"`, `"stackedCurves"`, or `"bar"`. |
| `Qualifier` | A 'namespace:term' qualifier string (e.g., 'bqbiol:hasPart', 'dc:title'). |
| `StringOrRef` | Any string. Note: any string starting with '#' is treated as an SIdRef. |
| `NumberOrRef` |  |
| `IntegerOrRef` |  |
| `PositiveIntegerOrRef` |  |
| `NonNegativeIntegerOrRef` |  |
| `PositiveDoubleOrRef` |  |
| `BooleanOrRef` |  |
| `URIOrRef` |  |
| `URNOrRef` |  |
| `KISAOIdOrRef` |  |
| `ScaleTypeOrRef` |  |
| `ListOfStringsOrRef` |  |
| `ListOfNumbersOrRef` |  |
| `ListOfAnyOrRef` |  |
| `AnyValueOrRef` | Any JSON value. Per the SED2 spec, an SIdRef string may substitute for any value. |

### Attribute details

**`SId`** - An identifier: starts with an English letter or underscore, may be followed by alphanumerics or underscores.

**`SIdRef`** - A reference to another SED element. Always starts with '#'. May include a colon-delimited path, dot-accessors (e.g. .model, .strings, .aggregates), and indexing ([n], [-n], ['label'], [a:b]).

**`KISAOId`** - A KiSAO identifier of the form KISAO:nnnnnnn (7 digits).

**`URI`** - A URI string. Can be absolute or relative.

**`URN`** - A URN string.

**`MarkdownString`** - A CommonMark-formatted markdown string.

**`NumberWithNaN`** - A number, Boolean, or one of the special strings nan / inf / -inf (case-insensitive), which represent NaN, +Infinity, and -Infinity respectively.

**`ScaleType`** - One of `"linear"` or `"log10"`.

**`CurveType`** - One of `"points"`, `"bar"`, `"barStacked"`, `"horizontalBar"`, `"horizontalBarStacked"`, or `"shadedArea"`.

**`SurfaceType`** - One of `"parametricCurve"`, `"surfaceMesh"`, `"surfaceContour"`, `"contour"`, `"heatMap"`, `"stackedCurves"`, or `"bar"`.

**`Qualifier`** - A 'namespace:term' qualifier string (e.g., 'bqbiol:hasPart', 'dc:title').

**`StringOrRef`** - Any string. Note: any string starting with '#' is treated as an SIdRef.

**`NumberOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`IntegerOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`PositiveIntegerOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`NonNegativeIntegerOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`PositiveDoubleOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`BooleanOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`URIOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`URNOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`KISAOIdOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`ScaleTypeOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`ListOfStringsOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`ListOfNumbersOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`ListOfAnyOrRef`** - _(no description yet - placeholder, needs to be filled in)_

**`AnyValueOrRef`** - Any JSON value. Per the SED2 spec, an SIdRef string may substitute for any value.


## Outputs

Not applicable - `Types` bundles primitive/reference-helper definitions; it is not itself an element with an id.

