# SBML

Language URN: `urn:sedml:language:sbml`.  (Whether level/version-specific
URNs are also accepted is not decided here.)

This folder records what SED2 needs to know about SBML models that the
generic specification cannot say.  One file per topic:

| File | Topic |
|---|---|
| `labels.md` | The SId namespace, and what a label or index on `.model` may refer to |
| `setValues.md` | The keys accepted in a ModelChange's `setValues` |
| `modelChange.md` | `addElements`, `removeElements` and `replaceElements` |
| `elementTypes.md` | The `includeTypes` / `excludeTypes` vocabulary of ModelElementList |
| `validation/` | Rules (`SBML-NNNN`), all `proposed` for now |

Anything marked "To be determined" has not been decided yet.  Until a topic
is filled in, validation must assume that anything is potentially valid.
