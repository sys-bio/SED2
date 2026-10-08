# SED2 TODO

Design questions that need real thought before the specification can be finalized.

## ModelChange: addElements and replaceElements (and the order of changes)

Raised while building pySED2Translate.

* `addElements`: the form of an entry is undefined.  The description says "e.g. an Antimony-formatted string for
  SBML".  Decide which languages are allowed, whether an entry is a fragment or a whole model, how it is merged into
  the model, and how its ids relate to the model's.  Other modeling languages will need their own rules.
* `replaceElements`: decide what a key and a value are (ids, or element text?) and what "internal references
  retargeted" covers.  The description already asks whether to keep this attribute at all, since add plus remove
  can do most of the same thing.
* State the order in which the four attributes (`setValues`, `removeElements`, `addElements`, `replaceElements`)
  are applied when a ModelChange has more than one.

Until this is decided, pySED2Translate skips any ModelChange that uses `addElements` or `replaceElements`, and
sed2-test-suite has no tests for them.

## AggregationCalculation: split into one class per function

Raised while building pySED2Translate (its GAPS.md S-006).

`AggregationCalculation` (and so a Repeat's `aggregateOutputVariables`) has `input` and `appliedDimensions` only;
`kisaoID` was folded into `_type` without a replacement, so nothing says whether to sum, average, take the standard
deviation, and so on.  Decision: split it into one class per aggregation function (core-spec section 10 lists the
planned split, "frozen for v1").

* Decide the list of functions (at least sum, mean, standard deviation, minimum, maximum, count).
* Each new class keeps `input` and `appliedDimensions`, and gets its own Data Sheet, outputs.json (the shape of
  `AggregationCalculation` today: the shape of `input` minus the applied dimension), rules and UML diagram.
* The same holds for the running statistics of a Repeat (`aggregateOutputVariables`).
* Update the AggregationCalculation rules (AggregationCalculation-000N), the Repeat rules that name it
  (Repeat-0009, Repeat-0010) and the fixtures.

Until this is decided, pySED2Translate cannot translate it: its capability table marks it unsupported (deferred) for
every backend, and a document with one is skipped (exit 11).

## CsvImport: attributes based on Python's readers

Raised while building pySED2Translate (its GAPS.md S-012).

The CsvImport prose is an unfinished sentence.  The author will draw a new CsvImport UML diagram with all the
options in it, and then the attributes are implemented from that diagram (schema, description, outputs.json, rules,
fixtures).  The proposal in the translator's GAPS.md bases them on `pandas.read_csv`, `numpy.loadtxt` and the `csv`
module:

| Proposed attribute | Python counterpart | Meaning / default |
|---|---|---|
| `location` | `filepath_or_buffer` | required |
| `separator` | `sep`, `delimiter` | one character; default `,` (use `"\t"` for tabs) |
| `headers` | `header=0` / `None` | true: the first line (after `skipRows`) holds the column names; default false |
| `columnNames` | `names` | labels for the columns when there is no header row (with a header row, replaces it) |
| `skipRows` | `skiprows` | number of leading lines to ignore (before the header); default 0 |
| `comment` | `comment`, loadtxt `comments` | a character that starts a comment running to the end of the line |
| `columns` | `usecols` | which columns to keep, by name (needs headers) or 0-based position; replaces `ncols` |
| `nrows` | `nrows`, loadtxt `max_rows` | read at most this many data rows (a limit, not an expectation) |
| `rowLabelColumn` | `index_col` | the column (name or position) whose values become the row labels |
| `missingValues` | `na_values` | strings read as `nan`; default: the empty cell, `nan`, `NaN`, `NA` |
| `decimal` | `decimal` | the decimal separator, default `.` |
| `quote` | `quotechar` | the quoting character, default `"` |
| `encoding` | `encoding` | default `utf-8` |
| `units` | (none) | units for the columns, metadata only |
| `organization` | `DataFrame.T` | `"columns"` (default: a series runs down a column) or `"rows"` (transposed) |

Open: whether `headers` should default to auto-detection (as pandas' `header="infer"`), and whether `ncols` should
be dropped.  Also open: `DataImport`'s `format` is a URI but no format URIs are defined, and the shape of its result
"depends on the file".

## Track the dimensions behind `trailing`

A `{"trailing": {"of": ...}}` entry in an outputs.json `dimensions` list marks dimensions that come from the output's own
entries (a Loop's `outputVariableMap` values, a CreateDataBlock's `data` values).  Validators treat them as unknown
today: indices that reach them are not checked, and they never make a reference "still shaped" (SEDBase-0015).

Eventually the validator should work them out: for each entry of the attribute named by `of`, follow the reference (to
a subTask output, a constant, another task, ...) or take the literal's shape, check that all entries have the same
shape, and append that shape.  That would also let SEDBase-0009/-0010/-0011/-0014/-0015 judge indices on the entries'
own dimensions, and report entries of different shapes before the document runs.

## TaskParameter: a `_type` that says which parameter it is

Decision: the thing that defines a TaskParameter is its `_type`.  For any parameter that the parent task does not
already define (as an attribute of its own), the `_type` should be a KiSAO id.  Not yet in the specification: today a
TaskParameter has only an id and a `value` (see `specsheets/*/TaskParameter`), and nothing says how an id names an
algorithm parameter.  When this is implemented, the TaskParameter schema and description change, `taskParameters`
gets its description, and libsed2 can expose it so that a translator can use it.
