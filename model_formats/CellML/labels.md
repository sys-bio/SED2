# CellML: labels

How a label on a model's `.model` output (e.g. `#tasks:mod1.model["V"]`) is
interpreted when the model's language is CellML.  See also
`specsheets/core/Types/v1.0.0/description.md`, "Elements of models".

## Namespaces

CellML has a single namespace for the top-level component.  The variables of
that component are the elements a SED2 label can name.

Elements of subcomponents (components nested by encapsulation, or imported
components) are officially inaccessible: the CellML specification treats a
component's encapsulated children as internal, so SED2 does not give them a
label, and no qualified form such as `"sub.x"` is defined.  To expose a value
from a subcomponent, the model itself must connect it to a variable of the
top-level component.

## Labels on `.model`

`#tasks:mod1.model["V"]` means the current value of the variable named `V`
in the top-level component.  The label must be a valid CellML identifier that
names such a variable.

## Numerical indexing

CellML variables are identified by name, not by position, so numerical
indexing of `.model` (e.g. `.model[0]`) is not defined.

## Open questions

* Whether and how a variable's value should be reachable when it is only
  exposed through an interface connection to a subcomponent is not decided.
* Variables that are constant versus computed (state, algebraic) are both
  addressable by label; whether a computed value is available at a given
  simulation point is the simulator's concern, not a validation rule.

Rules: CellML-0001, CellML-0002, CellML-0003 (in `validation/`).
