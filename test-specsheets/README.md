# test-specsheets/

A small, self-contained fixture tree - not part of the canonical spec (`specsheets/`, `core-spec.md`) - for exercising the code generator once it exists, without depending on the size or churn of the real spec. Layout mirrors `specsheets/` exactly (`core/`, `tasks/`, `outputs/`, `auxiliary/`, plus a `namespaces/` subtree mirroring the repo-root `namespaces/` layout), and every class here is a small, deliberately synthetic stand-in - none of it means anything - chosen to cover each of the composition patterns Design.md's Classes/Namespaces sections describe:

| Pattern | Fixture example(s) | Real-spec analog |
|---|---|---|
| Shared primitive/reference `$defs`, no class | `core/Types` | `core/Types` |
| Universal base mixin (name/description) | `core/TestBase` | `core/SEDBase` |
| Root/document class with dict-of-discriminated-union fields | `core/TestDocument` | `core/SEDDocument` |
| `x-generated-oneOf` discriminator + Common mixin (never itself instantiated) | `tasks/AbstractWidget`, `outputs/AbstractReport` | `tasks/AbstractTask`, `outputs/AbstractOutput` |
| Standalone schema-only mixin, no `oneOf` of its own | `tasks/WidgetOptions` | `tasks/AbstractSimulation` |
| Plain leaf branch(es) of a discriminator | `tasks/SimpleWidget`, `tasks/FancyWidget`, `outputs/SimpleReport` | `tasks/ExplicitODESimulation`, etc. |
| Simple embedded helper, no `_type`, not a branch of anything | `auxiliary/Note` | `auxiliary/TaskParameter`, `WorkingAlgorithm` |
| Directly-instantiable class that is also the root of further subclasses (Common mixin split + generated `inline` union) | `auxiliary/Choice` (+ `WeightedChoice` subtype) | `auxiliary/Range` (+ `NumericRange`, `ParameterRange`) |
| Namespace `new/` class (wholly new type) | `namespaces/acme/new/tasks/AcmeWidget` | (none registered yet) |
| Namespace `updated/` fragment (adds attributes to an existing class) | `namespaces/acme/updated/tasks/SimpleWidget` | (none registered yet) |

Every class folder follows the same Data Sheet shape as `specsheets/` (`schema.json` [+ `common.schema.json`/`inline.schema.json` where the pattern needs them], `description.md`, `validation/*.md`), except diagrams: since these classes don't mean anything, there's no UML to draw, so each folder carries a `DIAGRAM-PENDING.md` explaining that plainly rather than inventing one.

See Design.md's Specification Assembly section (and this README's own note there) for how this tree relates to the canonical `specsheets/`.
