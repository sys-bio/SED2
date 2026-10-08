# Types

*(This page bundles the shared primitive and reference-helper types; it has no single UML class box of its own - see `core/SEDBase` for the base class every element derives from.)*

**Category:** core  
**Schema:** [`schema.json`](./schema.json)

## What this covers

Every value in a SED2 document is either a literal value or a *reference* to a value elsewhere in the document. Anywhere the spec calls for, say, a `double`, that slot may instead hold a string reference such as `"#tasks:sim1.model['S1']"` that resolves to a double at read time. This page collects the primitive and reference-helper types used throughout the rest of the spec; it has no UML class of its own.

**Base value kinds.** Numbers (integers, doubles, etc.), Booleans, Strings, AnnotatedData (n-dimensional matrices of values with labeled coordinates and dimensions, modeled after `xarray.DataArray`), Models (a set of values/state plus the rules for how those values change), and Maps (a 1:1 mapping of one type to another, e.g. `{SId: SIdRef}`).

**Special number rules.** The strings `"nan"`, `"inf"`, and `"-inf"` (any capitalization) represent NaN, +Infinity and -Infinity respectively when found among numbers; a mix of strings and numbers in the same 1D AnnotatedData is an error unless every string is one of these three. Booleans may be parsed numerically as 1 or 0.

**References.** A reference is a `#`-prefixed, colon-delimited path following the document's hierarchical structure (e.g. `#tasks:sim1`, `#tasks:sim1[0]`, `#tasks:sim1.model["S1"]`, `#tasks:data_import["S1", 3]`, `#constants:time_end`). A task's own id always has an implicit `.model` accessor when it exports a model, and a `.strings` accessor when it exports a list of strings. AnnotatedData supports positional and label-based indexing (see Indexing), including comma indexing for selecting sub-slices of data.  *In the future, `.loc` (positional + coordinate label), `.isel` (dimension name + integer label), and `.sel` (dimension name + coordinate label), could be implemented, following the equivalent xarray/pandas/numpy conventions, but are not currently supported or officially defined.*

**Indexing.** All array data (AnnotatedData; array-based constants) can be sliced with indexes:
* `[n]` : the nth entry (0-based indexing)
* `[-n]` : the nth entry from the end, with '-1' meaning 'the last entry'.
* `['label']` or `["label"]` : The entry with the given label
* `[a:b]` : Entries a through b, including a but not including b.  a and/or b may be negative.
* `[a:]` : Entries from a to the end, including a
* `[:b]` : Entries from the beginning to b, not including b
* `[:]` : All entries
* `[<anything>, <anything>, ...]` : For multiple dimensions, applies the first index to the first dimension, the second index to the second, etc.  For `[a:b, n]`, this would mean that the index `a:b` would apply to the first dimension and the index `n` to the next one, like numpy's `x[a:b, n]`, so it gives entry `n` of each selected entry.  Labels may be used here, as well as any other index form.
* `[a:b][<anything>]` : Any time brackets are followed by brackets, the second brackets apply to the entire object defined by the first set of brackets.  An integer or label index removes its dimension from the result; a range keeps it, narrowed to the selected entries (and their labels).So `data[2:5][0]` is the same as `data[2]`, since the first bracket gives you 'the third through fifth rows of data' which has the same dimensionality that `data` had in the first place.  So the `[0]` still means 'the first row of that', which is the third row.  So it's not usually very helpful to have a ranged bracket followed by another bracket: you probably instead want the comma form, above: `data[2:5, 0]` means 'the first entry of the third through fifth elements of data'.  `data[3][5]` gives you the sixth entry of the fourth row of the original data, which *is* useful, and is exactly equivalent to `data[3, 5]`, because the single `3` reduced the dimensionality of `data`.

Any indexing must select at least one entry.  Whitespace is allowed.

**Elements of models.**
The current numerical value of an element of a model may be obtained by label, i.e. `#tasks:mod1.model["S1"]`.  Every model format (i.e. SBML, CellML) must define its own set of legal labels to access its internal elements, but it will generally be true that `"S1"` will mean "The element with the id "S1" in the model," regardless of format.

A format-aware library will be able to validate these references, checking (for example) whether "S1" is indeed the id of an element in the referenced model.

It is possible that some model formats will allow numerical indexing, or disallow label indexing.  See model_formats/ for more information.  If no information is available for a given modelling language, validation must assume that any indexing scheme is potentially valid.

## Attributes

Not attributes of a class - `Types` instead bundles the following primitive/reference-helper `$defs`, each usable via `$ref` from any other Data Sheet's schema:

| Name | Description |
|---|---|
| `SId` | An identifier: starts with an English letter or underscore, may be followed by alphanumerics or underscores. |
| `SIdRef` | A reference to another SED element. Always starts with '#'. May include a colon-delimited path, dot-accessors (e.g. .model, .strings, .aggregates), and indexing (see Indexing). |
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

**`SIdRef`** - A reference to another SED element. Always starts with '#'. May include a colon-delimited path, dot-accessors (e.g. .model, .strings, .aggregates), and indexing (see Indexing).

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

