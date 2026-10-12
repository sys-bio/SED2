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

## Reporting a dictionary constant or a whole model; labels of `[id].aggregates`

Raised while porting the old sed/ test templates to the current specification (sed2-test-suite/templates/PORTING.md).

* `constant_dict_list` and `constant_dict_num` reported a dictionary constant directly (`"data": "#constants:X"`).
  Validation now rejects that (SEDBase-0017: the reference "resolves to an object, not AnnotatedData"), while
  `createDataBlock` with `"data": "#constants:X"` is accepted and gives the same labelled data.  Is the rejection the
  intent?  If so a dictionary constant is data only inside a CreateDataBlock or when indexed (`#constants:X['S1']`).
* `model_full_output` reported a whole model (`"data": "#tasks:model1.model"`), which the old tests meant as "a list
  of model ids and their values".  That is rejected for a Report and for a CreateDataBlock.  There is no way left to
  get all the values of a model at once; `modelElementList` gives only the ids.  Intended?
* `#tasks:repeat.aggregates['avg_sim']['S1']` (the keys of `aggregateOutputVariables` as the labels of the first
  dimension of `[id].aggregates`) fails SEDBase-0010 with "uses label avg_sim, which is not one of: " (an empty list),
  although `#tasks:repeat.aggregates[0]['S1']` and `#tasks:repeat.aggregates` validate.  Either the keys should be
  accepted as labels (this is what the old template did) or the description should say that the dimension is
  positional.  Possibly the same cause as "Track the dimensions behind `trailing`" above.
* The old `outputModel` attribute on tasks has no counterpart; `.model` is simply available.  Noted, not a question.

## References inside list and dictionary constants

Raised while writing sed2-test-suite cases for constants.

`AnyValueOrRef` is recursive and says "an SIdRef string may substitute for any value", so a constant such as
`"b": ["#constants:a", 6]` or `"b": {"k": "#constants:a"}` is valid.  The specification does not say what it means.
Is the string replaced by the value it refers to (so `b` is the vector 5, 6)?  Or is it only a reference when it is
the whole value of a constant (or of an attribute such as `setValues` entries), and an ordinary string inside a list?
If it is replaced, what happens when the referred value is itself a list (a ragged or nested result)?

pySED2Translate refuses such constants with a message pointing here, rather than guess.  No test case covers this
until the specification says what is meant.

## RelabelData: references that index by the new labels are rejected

Raised while writing sed2-test-suite cases for RelabelData.

`RelabelData`'s outputs.json says its result has "the same dimensions as the referenced input" (`shapeOf(input)`), so
the validator takes the labels of the *input* as the labels of the result.  A reference that uses one of the new
labels is rejected:

    "blk": {"_type": "createDataBlock", "data": {"a": 1, "b": 2, "c": 3}},
    "rel": {"_type": "relabelData", "input": "#tasks:blk", "labels": ["x", "y", "z"]}
    ... "data": "#tasks:rel['y']"      -> SEDBase-0010: uses label y, which is not one of: a, b, c.

while `#tasks:rel['b']` (an old label) is accepted, which is the wrong way round.  The same happens for labels given by
a constant (`"labels": "#constants:names"`) and for labels from a StringFormation `.strings`, and for a relabelled
matrix.  The labels of dimension 0 of the result should be the `labels` attribute (when it is a literal list, or a
reference to a constant), and unknown when it comes from a task.  Until then the suite has no case that indexes by a
new label.

## Math: results the specification does not state

Raised while writing sed2-test-suite cases for Calculation.  None of these has a test case yet; each is a place where
a library must pick a behaviour.  What pySED2Translate does today is given in brackets; proposals only.

* Division by zero and arguments outside a function's domain: `1/0`, `0/0`, `ln(0)`, `ln(-1)`, `root(-1)`,
  `arcsin(2)`, `factorial(-1)`, `factorial(2.5)`, `exp(1000)`.  Proposal: IEEE 754 results (infinities and NaN, no
  error).  [IEEE results: inf, nan, -inf, nan, nan, nan, nan, nan, inf.]
* `quotient` with a negative operand: `quotient(-7, 2)` is -3 (truncated) or -4 (floored)?  MathML says "integer part
  of a/b".  [-3.]
* `arccot` of a negative number: `arccot(-1)` is -pi/4 (arctan(1/x)) or 3pi/4 (range 0 to pi)?  [-pi/4.]
* A comparison or logical expression that is the whole result of a Calculation (`"math": "3 < 4"`): the result is a
  boolean, and the specification only says booleans "may be parsed numerically as 1 or 0".  Proposal: say that the
  result is the number 1 or 0.  The suite wraps tests in `piecewise(1, test, 0)` until then.
* A relational operator with a vector operand inside `piecewise` (`piecewise(1, v < 2, 0)`): is the condition applied
  element by element, as every other operation is?  [yes: the result is a vector.]
* Two operands with labels: if one is labelled and the other is not (`blk + #constants:v`), is the result labelled?  If
  both are labelled with different labels, is that an error?  Does a dictionary constant combine with another one of
  the same keys in a different order by key or by position?  (The suite only combines identical key lists.)
* `RelabelData` on data without labels: does it add labels?  With the wrong number of labels, is that an error?
* `CreateDataBlock` entries that carry labels of their own (a labelled vector as an entry): are those labels kept as
  labels of dimension 1 of the block?
* `StringFormation` of numbers whose shortest decimal needs an exponent (`1e-7`, `1e21`): is it `1e-07`, `1e-7`,
  `0.0000001`?  The description says "the shortest decimal that reads back as the same number", which does not settle
  the notation.  The suite avoids such numbers.

## Time courses: points the specification does not state

Raised while writing sed2-test-suite cases for ExplicitODESimulation, OneStepODESimulation and BoundedODESimulation.
Proposals only; what pySED2Translate does today is in brackets.

* The label of the first column is `independentVariable` as written (outputs.json: `[independentVariable] + outputVariables`),
  so with `urn:sedml:symbol:time` the column is labelled `urn:sedml:symbol:time`.  Is that intended, or should the symbol
  have a friendlier label such as `time`?  [The label is the text as written.]
* Is `"independentVariable": "time"` (without the URN) valid?  The description of SteadyState says "either the model's own
  variable, or an implicit URN such as `urn:sedml:symbol:time`".  [Both spellings are run as time.]
* `independentVariableInit` is not described.  When it is missing, does the model start at the first output point (so
  the first row shows the initial state), or at 0?  [The first output point; the suite always gives it when the first
  point is not 0.]  When it is given and is before the first output point, the model is integrated from it to that point
  without output.
* An algorithm that works with a fixed step (KISAO:0000032 Runge-Kutta 4, 0000030 Euler) with no `initialStepSize`: which
  step does it use?  Results then depend on the simulator (roadrunner and OpenCOR differ by 2e-4 on a simple decay), so
  the suite compares such a case loosely.
* A simulator that cannot honour one of the optional solver settings (for example `useStiffSolver` with LSODA): must it
  fail, or may it ignore the setting?  [The translator skips the task, naming the setting.]
* `BoundedODESimulation` has "solver-chosen" output rows, so only its end can be compared between simulators.  Should the
  first row be required to be the initial state, and the last row to be exactly the end of the span?  [Both hold for
  roadrunner and COPASI.]
* A species with no initial amount or concentration in the SBML file (Antimony leaves it unset) is "undefined" in SBML,
  and the simulators disagree about it: roadrunner starts it at 0, COPASI and OpenCOR at 1.  Not a SED2 question; the
  suite sets every initial value.

## Steady states and Jacobians: points the specification does not state

Raised while writing sed2-test-suite cases for SteadyState, JacobianFull and JacobianReduced.  Proposals only; what
pySED2Translate does is in brackets.

* **JacobianReduced: which species are dropped?**  The description says "a reduced subset of species" with no rule.  For
  A <-> B (A + B conserved) the reduced matrix is 1 x 1 for A or for B, and the labels differ.  [roadrunner and COPASI both
  keep the first species of each conservation law, so the cases in the suite assume the same.]  Proposal: say that the
  reduced set is the independent species of a conservation analysis, and either fix the choice (for example the species
  that come first in the model's order) or say that the labels of the result identify which were kept.
* **Concentration or amount?**  A Jacobian entry d(dx_i/dt)/dx_j is the same for concentrations and amounts only when every
  compartment has volume 1.  [The id of a species means its concentration, as everywhere else in SBML (and its amount if
  hasOnlySubstanceUnits), so entries are concentration based.]  Proposal: state it.  The suite uses volume 1 only.
* **Boundary species.**  Does the Jacobian have rows and columns for species with `boundaryCondition="true"`, or only for
  the species that change?  [Only the floating species.]
* **Initial state.**  The Jacobian is taken at the model it is given: the initial state of an imported model, or the end
  state of an earlier task (`"model": "#tasks:s.model"`).  [As described.]  Proposal: say so.
* **SteadyState with several steady states**, and with a stable and unstable one: which does it find?  The suite starts
  close to the steady state it expects.  A solver that fails to converge should fail the task, not return the last iterate.
* **COPASI and a species whose value is exactly zero:** COPASI's Jacobian is wrong for such a species (not a SED2
  question; recorded as D-001 in sed2-test-suite/disagreements.json).

## ModelChange for SBML, CsvImport and plots: points the specification does not state

Raised while writing sed2-test-suite cases for ModelChange, CsvImport, Plot2D and Plot3D.  Proposals only; what
pySED2Translate does is in brackets, and the cases keep to what is clear.

* **setValues, SBML keys** (model_formats/SBML/setValues.md is "to be determined").  Setting a species id: is it the
  initial concentration or the initial amount?  [Concentration, or amount if hasOnlySubstanceUnits, as for the labels of
  `.model`.]  The suite sets species only in compartments of volume 1.  Setting an element that has an initial assignment
  [the assignment is dropped and the value used], or that is the target of an assignment or rate rule [not decided].  The
  grammar of keys such as `"S1.boundary"` and `"S1.constant"` [accepted, value 0 or 1].  Not tested.
* **removeElements, SBML** (model_formats/SBML/modelChange.md is "to be determined").  Which element kinds may be removed,
  and what happens to elements that still refer to a removed one (a species used by a reaction, a parameter used by a
  kinetic law)?  [Any SBML element listed by id may be removed; nothing else is changed; an id the model lacks fails the
  task.]  The suite removes reactions only.
* **A ModelChange of a simulation's `.model`.**  Does it keep the simulated end state and apply the change on top of it?
  [Yes.]  Proposal: say so in ModelChange and in the description of the simulations' `[id].model`.
* **The flux label.**  `.model['J']` for a reaction is "its current flux": in amount per time (the value of the kinetic law)
  or concentration per time?  [The kinetic law's value.]  The suite uses a compartment of size 2 for this one.
* **CsvImport.**  The description is a placeholder.  Open: the default of `headers`; a header line together with
  `columnNames` (which wins); `nrows` or `ncols` larger than the file (an error, or all that is there?); whether `nrows`
  counts the header line; blank lines, a byte order mark, spaces around names and numbers; the number forms accepted
  (`1e-3`, `.5`, `nan`, `inf`); whether an empty cell is an error or NaN.  [Header excluded from `nrows`; blank lines
  skipped; the header names win over `columnNames`; larger limits fail; an empty cell fails.]  The suite tests plain
  numbers, `separator`, `headers`, `columnNames` alone, `nrows` and `ncols` within the file size, and exponent forms.
* **Plot2D: a curve with no `order`.**  Where does it go among curves that have one?  [Treated as order 0.]  Not tested; the suite gives every
  curve in a multi-curve plot either an order or none of them an order.
* **Plot3D: the shape of `z`.**  For `x` with n values and `y` with m values, is `z` m x n (rows follow `y`) or n x m?
  And must the shapes agree at all?  [Not checked; the suite uses m x n.]  Also whether a surface of type
  `parametricCurve` needs three vectors of the same length.

## ModelElementList and the labels of repeats: points the specification does not state

Raised while writing sed2-test-suite cases for ModelElementList and the repeat tasks.  Proposals only; what
pySED2Translate does is in brackets.

* **ModelElementList: the order of the ids.**  `[id].strings` is a list, but nothing says how it is ordered.  [Model
  order: the order in which the SBML file lists species, compartments and so on, grouped by element kind.]  Proposal:
  say that the order is that of the model format (and define it per format in `model_formats/<format>/elementTypes.md`) or
  that it is sorted.  The suite selects one element, so the order cannot matter, and has no case for a longer list.
* **ModelElementList: the type vocabulary for SBML** (`model_formats/SBML/elementTypes.md` is "to be determined"):
  only `"species"` appears, as an example.  [Species, compartment, parameter, reaction and the other SBML element
  kinds, spelled in lower case; an unknown type fails the task.]  Also what an id that the model does not have does in
  `includeElements` or `excludeElements`: an error, or is it ignored?  [An error.]  Only `"species"` is used in the suite.
* **Repeat labels with repeated values.**  The iterations of a Scatter or Loop are labeled by the range values.  When a
  range repeats a value (`values: [1, 1, 2]`), two labels are equal and `[id]['1']` is ambiguous.  [The first match.]
  Proposal: say what a label index does in that case (first match, or an error), or that a range used by a repeat must
  have distinct values.  The suite uses distinct values only.

## Flux balance analysis and the cosimulation template: points the specification does not state

Raised while adding FluxBalanceAnalysis to pySED2Translate (COBRApy backend) and writing sed2-test-suite cases 00274-00282.
Proposals only; what pySED2Translate does is in brackets.

* **Infeasible (or unbounded) problems.**  What does a FluxBalanceAnalysis task give when the linear program has no optimum?
  This happens in the real cosimulation: once glucose is exhausted, iAF1260's ATP maintenance reaction (a positive lower
  bound) cannot be supplied.  [The task fails with the solver status in the message; no values are reported.]  Proposal:
  say that the task fails, or define a status output.  Not tested in the suite.
* **`[id].model` of a FluxBalanceAnalysis.**  The description says "the resulting model state"; an FBA changes no value
  of an SBML model.  [The model that went in, unchanged.]  Proposal: say so, or say what state an FBA adds (for example the
  fluxes as reaction values).  Not tested in the suite.
* **Output variables that are not reactions.**  `outputVariables` are "model variables (usually fluxes)".  [A reaction
  gives its flux; a parameter, compartment or species gives the model's value; anything else fails.]  Case 00277 reads a bound
  parameter.
* **Which models can be analysed, and the bounds.**  FBA needs an objective and bounds, which the SBML FBC package carries;
  the specification does not say that the model must have it.  [A model without FBC is skipped, exit 11.]  Bounds are parameters
  (`fbc:lowerFluxBound="R_EX_glc__D_e_lower_bound"`), so ModelChange `setValues` changes them; COBRApy shares one parameter
  among all reactions with the same default bound, so a document should give a reaction its own parameter before changing it.
* **`workingAlgorithms` of an FBA.**  Only the generic KISAO:0000437 is accepted.  The LP solver (glpk, scipy) is not part of
  the algorithm; pySED2Translate chooses it as a backend variant (`cobra:glpk`).  Also, flux distributions are often not
  unique, so results of different solvers can legitimately differ for variables with alternative optima; the suite's cases
  have unique optima.
* **templates/cosimulation.sed2.json.**  (1) `setValues` takes the whole last row of the ODE result (`odesim[-1]`), but that row
  has a time column (`urn:sedml:symbol:time`), which is not an element of the FBA model; a ModelChange from a labeled row needs a
  rule for labels the model lacks (error, or ignored), or the template should select the elements.  [Case 00282 hands over
  one named element.]  (2) The report `#tasks:repeat['species_trace']` indexes dimension 0, which is the iteration; the entry is
  dimension 1, so `repeat[:, 'species_trace']`.  (3) `numericRange` with only `numberOfSteps: 100` gives 101 iterations and
  needs a `start` and an `interval` (it has neither).  (4) The template names `FBA_rxns` with `includeTypes: ["reactions"]`; the
  SBML vocabulary spells the type `reaction`.  [Case 00276 uses `reaction`.]

## Metabolic control analysis and related analyses: the functions to consider besides the Jacobian

Raised while looking at what roadrunner and COPASI offer next to the Jacobian (JacobianFull and JacobianReduced are the first of a family).  Proposals only; nothing is implemented in pySED2Translate.  What was observed is in brackets, from running libroadrunner 2.10.0 and copasi-basico 0.88 on the model at the end of this section.  The KiSAO ids in the last column of the table were looked up in a local copy of KiSAO (git commit f0417f8, 2026-03-31), where they are the "systems property" classes 0000801 to 0000819 and 0000835 under 0000800; they should be checked against the current release before use.  Only 0000812 (full Jacobian) and 0000809 (reduced Jacobian) are used here already.

* **What the roadrunner API holds.**  Everything below is a method of `roadrunner.RoadRunner`; the C++ declarations are in `source/rrRoadRunner.h`.

| Quantity | roadrunner | COPASI (basico) | Result: rows x columns, labels | Needs a steady state | KiSAO id (local copy) |
| --- | --- | --- | --- | --- | --- |
| Full Jacobian (specified) | `getFullJacobian` | `get_jacobian_matrix` | species x species | no, the state as given | 0000812 (already used here) |
| Reduced Jacobian (specified) | `getReducedJacobian(h)` | `get_reduced_jacobian_matrix` | independent species x independent species | no | 0000809 (already used here) |
| Eigenvalues of the full and the reduced Jacobian | `getFullEigenValues`, `getReducedEigenValues`, and `...NamedArray` versions | no function found by name | one row per species, columns `real` and `imaginary` | no | 0000813 (full), 0000810 (reduced) |
| Stoichiometry matrices | `getFullStoichiometryMatrix`, `getReducedStoichiometryMatrix` (the same as `getNrMatrix`), `getExtendedStoichiometryMatrix` (with boundary species), `getReactantsStoichiometryMatrix`, `getProductsStoichiometryMatrix` (both with an optional `boundary`) | `get_stoichiometry_matrix`, `get_reduced_stoichiometry_matrix` | species x reactions | no, structural | 0000811 (full), 0000808 (reduced), 0000819 (Nr); none for the extended, reactants and products matrices |
| Conservation analysis | `getLinkMatrix` (L), `getL0Matrix` (L0), `getKMatrix` (K, the nullspace of Nr), `getConservationMatrix` (Gamma), `getConservedMoietyIds`, `getConservedMoietyValues` | only the reduced stoichiometry matrix | L: species x independent species; L0: dependent x independent species; K: reactions x kernel columns; Gamma: conserved sums x species | no, structural | 0000816 (link matrix L), 0000818 (L0), 0000817 (kernel K); none for Gamma, the moiety ids or the moiety values |
| Elasticities, unscaled and scaled | `getUnscaledElasticityMatrix`, `getScaledElasticityMatrix`; one value: `getuEE`, `getEE` (a reaction against a parameter or species), `getUnscaledParameterElasticity`, `getScaledFloatingSpeciesElasticity`, `getUnscaledSpeciesElasticity` | `get_elasticities(scaled)` | reactions x species | the state as given (see below) | matrices: 0000804 (unscaled), 0000806 (scaled); single coefficients: 0000805 (unscaled), 0000807 (scaled) |
| Concentration control coefficients, unscaled and scaled | `getUnscaledConcentrationControlCoefficientMatrix`, `getScaledConcentrationControlCoefficientMatrix` | `get_concentration_control_coefficients(scaled)` | species x reactions | yes | 0000801 (unscaled), 0000835 (scaled) |
| Flux control coefficients, unscaled and scaled | `getUnscaledFluxControlCoefficientMatrix`, `getScaledFluxControlCoefficientMatrix` | `get_flux_control_coefficients(scaled)` | reactions x reactions | yes | 0000814 (unscaled), 0000815 (scaled) |
| Control coefficient of one variable with respect to one parameter | `getuCC`, `getCC` (the variable is a reaction or a floating species; the parameter is a global parameter, a boundary species or a conserved sum) | the sensitivities task: `run_sensitivities`, `get_scaled_sensitivities`, `get_unscaled_sensitivities` (not compared) | one number | yes | 0000803 (unscaled), 0000802 (scaled) |
| Frequency response | `getFrequencyResponse(startFrequency, numberOfDecades, numberOfPoints, parameter, variable, useDB, useHz)` | no function found by name | points x 3, unlabeled | yes | none |
| Time-course sensitivities | `timeSeriesSensitivities` (a forward sensitivity solver, the only one registered) | the sensitivities task | one matrix per time point | no, a time course | none specific; 0000650 (sensitivity) is a general property, not a matrix |
| Rates of change | `getRatesOfChange`, `getIndependentRatesOfChange`, `getDependentRatesOfChange`, and `...NamedArray` versions | not looked at | one value per species | no | 0000834 (rate of change, of one variable with respect to another; not specific to the species vector) |
| Lyapunov exponents | none | `run_lyapunov`, `get_lyapunov_exponents` | | no | none |

* **The simulator settings behind them.**  `diffStepSize` (default 0.02, the step of the numerical derivatives), `steadyStateThreshold` (0.01), `fluxThreshold` (1e-9; below it a scaled flux control coefficient is returned as 0), the conserved moiety analysis switch (`conservedMoietyAnalysis`, off by default) and the steady-state solver.  [With the switch off, `getReducedJacobian` returned the full 4 x 4 matrix of the model below; with it on, a 3 x 3 matrix over S1, S2 and S3.  So the meaning of "reduced" depends on a setting that is not part of the model.  COPASI's reduced Jacobian is 3 x 3.]  Proposal: say which of these are parameters of the algorithm (and so go with a KiSAO parameter id on the task's algorithm, as for the integrators) and which are fixed by the specification.
* **One class per quantity, as for the Jacobian.**  JacobianFull and JacobianReduced were split to avoid a flag.  By the same rule the elasticities, concentration control coefficients and flux control coefficients would each be two classes (scaled and unscaled), which is six, plus the rest of the table.  Proposal: do the same split, each class with only a `model` attribute (and a `parameters` list where the quantity is taken with respect to parameters), and an output that is a matrix labeled with SBML ids (species in `listOfSpecies` order without boundary species, reactions in `listOfReactions` order, as in `model_formats/SBML/jacobian.md`).
* **Which of them need a task at all.**  Only quantities that need the meaning of the model are tasks: the Jacobian, the stoichiometry matrices, the elasticities (derivatives of the rate laws) and the derivatives with respect to parameters.  The rest is linear algebra on those: the eigenvalues are a function of the Jacobian output; L, L0, K and Gamma follow from the stoichiometry matrix; and the control coefficients follow from the stoichiometry matrix and the elasticities (the standard formulas, with N, E, L and K).  Proposal: add tasks for the first group and consider `eigenvalues`, `inverse` and `nullspace` as functions of `Calculation`, so that any simulator that gives the Jacobian or the elasticities (OpenCOR for the Jacobian, once it does) can give the rest.  A consequence to decide: the choice of dependent species in L (the same open point as in `jacobian.md` for the reduced Jacobian) then moves into those functions.
* **The state they are evaluated at.**  Control coefficients are defined at a steady state.  [Observed: roadrunner's matrix functions first bring the model to a steady state and leave it there (S1 went from 1.0 to 5.45 on a fresh model); the one-value functions `getuCC`, `getCC` do not move the model.  `getCC('J3', 'k1')` gave 0.99999999 after `steadyState()` and 7.27 on a fresh model, which is the unscaled value: the scaling uses the flux and parameter values at the current state, not at the steady state it computed the derivative at.  So the same call answers differently depending on where the model is.]  Proposal: say that, like the Jacobian, the quantity is evaluated at the model's state as given, that a document gets a steady state with a SteadyState task first, and that a control coefficient asked at a state that is not a steady state fails, with a tolerance on dx/dt stated in the specification; and note the roadrunner behaviour for consumers.
* **Scaled quantities at a zero.**  A scaled coefficient divides by a flux or a concentration, which can be zero (a reaction at equilibrium).  [Observed: in the model below reaction J4 (S3 -> S4) is at equilibrium, and the steady-state flux comes out as -4.4e-16, which is rounding error.  The scaled elasticities of J4 for S3 and S4 are then the unscaled ones (1 and -2) divided by that number, 6.0048e15 in magnitude, in both roadrunner and COPASI; the value is set by the rounding error and so may differ between platforms.  roadrunner guards the zero in `getCC` and in the scaled flux control coefficient matrix with `fluxThreshold` (the result is 0), but the scaled elasticities have no such guard.  For the scaled flux control coefficient of J4 with respect to itself roadrunner gives 0 and COPASI gives 1.0, while COPASI's own unscaled value is 1e-16; the scaling factor v/J is exactly 1 for a reaction against its own flux, so COPASI's scaled and unscaled values disagree with each other.  The true value is 0/0: the unscaled derivative is 0 at an equilibrium, and the scaled limit depends on how it is taken.]  Proposal: define the result at a zero denominator as an error (the task fails, as for the COPASI Jacobian at a zero-valued species, D-001 in sed2-test-suite) or as NaN, and not a very large number or a convention-dependent 0 or 1; say which, so that the two simulators cannot differ silently; and give the threshold below which a flux counts as zero (roadrunner: `fluxThreshold`, 1e-9) as a parameter or as part of the specification.  For a test suite, keep J4 as the zero-flux case and take the ordinary values from J1 to J3, which agree in the two simulators.
* **Species values: amount or concentration.**  The Jacobian already says that a species' value is its concentration, or its amount with `hasOnlySubstanceUnits`.  Elasticities and control coefficients with respect to species need the same statement.  [Neither roadrunner's bare species id (an amount) nor COPASI's `[id]` (a concentration) follows the flag in a selection; the matrix functions above were only run on a model with compartment size 1, so whether they follow it was not checked.]
* **Labels.**  [roadrunner labels rows and columns with SBML ids (`J1`, `S1`) and the eigenvalue rows with the species ids; COPASI labels reactions as `(J1)` and adds a column `'Summation Error'` to the control coefficient tables.]  Proposal: SBML ids only, no extra columns (the summation theorems are checks a document can compute).
* **Parameter-targeted quantities.**  `getCC(variable, parameter)` takes global parameters, boundary species and conserved sums, which are not reactions, so the matrices above (all with respect to reactions) do not cover it.  Proposal: a separate class with a `parameters` list (a ModelElementList) and an output variables x parameters matrix, if wanted; it is the same shape as COPASI's sensitivities output.
* **Frequency response and sensitivities.**  `getFrequencyResponse` returns an unlabeled 3-column table (its meaning of the columns is not documented in the header, only its arguments), and `timeSeriesSensitivities` returns a tuple.  Proposal: leave both out until there is a use; they are dynamic, not steady-state quantities.
* **Support.**  Both roadrunner and COPASI cover the control coefficients and elasticities, and the values agreed on the model below where compared (concentration and flux control coefficients, elasticities, Jacobians), except for the zero denominators above.  OpenCOR and COBRApy offer none of these; for the Jacobian-based ones through OpenCOR this was not checked.
* **What the local KiSAO already says.**  The classes 0000801 to 0000819 and 0000835 are all "systems property" classes (sub-classes of 0000800), so a result is identified by the quantity, not by the algorithm.  Their definitions are thin: 0000816 to 0000819 (link, kernel, L0, Nr) say only "the X matrix of a model", with no dimensions or labels; 0000808 (reduced stoichiometry) says "species by reactions" although it has only the independent species as rows; 0000808 and 0000819 (Nr) look like the same matrix (roadrunner returns the same one for both).  0000802, 0000803, 0000805 and 0000807 are single coefficients with a "dependent element" (reaction or floating species) and an "independent element" (global parameter or boundary species), matching `getCC`, `getuCC`, `getEE` and `getuEE`.  0000836 to 0000838 (amount, particle number, concentration) exist and could carry the amount-or-concentration choice above.  Proposal: add ids for the quantities marked "none" in the table that are wanted (the conservation matrix Gamma, the extended, reactants and products stoichiometry matrices, the frequency response) and tighten the definitions above, as a request to the KiSAO maintainers.

The model used for the observations (Antimony; S3 and S4 form a conserved pair):

```
model m
  J1: $Xo -> S1; k1*Xo - k2*S1;
  J2: S1 -> S2; k3*S1 - k4*S2;
  J3: S2 -> $X1; k5*S2;
  J4: S3 -> S4; k6*S3 - k7*S4;
  Xo = 10; X1 = 0; S1 = 1; S2 = 1; S3 = 3; S4 = 1;
  k1 = 1; k2 = 0.5; k3 = 2; k4 = 0.5; k5 = 1; k6 = 1; k7 = 2;
end
```

## Namespaced `pbg@` tasks: a real test of the namespace mechanism (low priority)

One possible use of SED2's namespaces is carrying what has no SED2 equivalent when a Process Bigraph document is imported (the pbg2sed2 translator). The importer itself does not translate partially: a document with a part that has no translation is refused whole, and its report lists the parts. This item is the optional follow-up, to be done after the clock proposals and the other items above, if a test of the namespace rules is wanted.

The idea: a class-level namespace `pbg` (`_type: pbg@process`, `pbg@step`, and so on) whose tasks hold a node as it is in the Process Bigraph document (address, config, inputs and outputs with their wires, interval) next to the SED2 tasks that the importer could translate, so that the whole document survives in one SED2 file. What this would exercise in the specification (section 7 and rules SEDDocument-0009 and 0010): a reader that does not know `pbg` keeps the content opaque and passes it through unchanged; a `pbg@version` attribute is required on the document; a `namespaces/pbg/` schema is composed at generate time and validated by tools that know it; and a round trip (import, then export back to Process Bigraph) can be checked against the original document.

Not decided and not needed yet: whether a `pbg@` task takes part in the SED2 task graph (references to and from SED2 tasks), whether the namespace should be defined in this repository or in pbg2sed2, and what the version of the namespace means. The three questions can wait until the item is taken up.
