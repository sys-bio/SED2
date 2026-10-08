# SBML: labels

How a label on a model's `.model` output (e.g. `#tasks:mod1.model["S1"]`) is
interpreted when the model's language is SBML.  See also
`specsheets/core/Types/v1.0.0/description.md`, "Elements of models".

## Namespaces

SBML uses an `SId` namespace for most mathematically relevant elements.  In
SBML Level 3 that namespace covers, within one model, the `id` of: the
function definitions, unit definitions, compartments, species, global
parameters, reactions, rules' targets (by variable), and the elements of
packages that declare ids in the same namespace.  Ids in this namespace are
unique within the model, which is what makes a bare label unambiguous.

The main exception is the local parameters of reactions (`localParameter`, or
`parameter` in a kinetic law before Level 3).  Their ids are scoped to the
reaction that holds them: two reactions may each have a local parameter named
`k`, and a local parameter may share an id with a global element.  A local
parameter is therefore not reachable through a bare label.

## Labels on `.model`

`#tasks:mod1.model["S1"]` means the current value of the element whose `SId`
is `S1`, for example:

* a species: its amount or concentration, as the model defines it;
* a compartment: its size;
* a global parameter: its value;
* a reaction: its current flux.

The label must be a valid `SId` that exists in the model's `SId` namespace.

## Numerical indexing

SBML has no ordered, numbered collection of such elements that is part of the
format, so numerical indexing of `.model` (e.g. `.model[0]`) is not defined.

## Open questions

* How to address a reaction's local parameters (for example a qualified label
  `"reaction1.k"`) is not decided; until it is, such references are not valid.
* Which element kinds beyond species, compartments, global parameters and
  reactions are meaningful targets (for example stoichiometries given by
  rules) is not decided.

Rules: SBML-0001, SBML-0002, SBML-0003 (in `validation/`).
