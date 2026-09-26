# test-specsheets/fixtures/

Document-level fixtures for exercising the code generator itself, once it
exists: generate the three libraries from `test-specsheets/` (see that
folder's own README) and run these fixtures through each generated
library's parser + `validate()`, the same way the real `fixtures/` tree
(see Design.md's Testing section) exercises the generated libraries
against the real spec - just scoped to this small, synthetic tree instead,
so a generator change can be tested without depending on the size or
churn of the real spec.

Naming follows Design.md's fixture convention exactly:
`<rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>...].sed2.json`.
`pass`/`fail` says whether the document should validate; `count` is how
many times the leading rule is expected to fire (`00` for a pass case);
chained rule IDs at the end each carry their own count. A pass fixture
needs no companion expected-output file - the check is that the document
parses and re-serializes unchanged (see Design.md's Testing section for
the exact comparison rules: key order, numeric tolerance, etc.) - and a
fail fixture is checked against the specific rule ID(s) and count(s)
its filename encodes.

Every one of `test-specsheets/`'s 37 numbered rules has a fail fixture
here, except six `_type`-discriminator-const rules (`Choice-0002`,
`WeightedChoice-0002`, `SimpleWidget-0002`, `FancyWidget-0002`,
`acme-AcmeWidget-0002`, `SimpleReport-0002`). Those six validate the
class's own schema directly rather than embedded through its parent
discriminator's dict field (`widgets`/`reports`/`choices`): once a
`_type` value fails to match a branch's own `const`, it no longer
identifies *any* branch, so the failure is the *discriminator's* own
generic catch-all (e.g. `AbstractWidget-0000`) or its missing-`_type`
rule, never one specific sibling's own `-0002` - the same way a real
`_type` mismatch inside `tasks` can only ever resolve to `AbstractTask`'s
own catch-all, never to one guessed concrete class (see Design.md's
Schema-Pass Errors section). A leaf's own `_type`-const rule is only
ever reachable by validating that one class directly, so its fixture
here is the bare class instance rather than a whole `TestDocument`.

`Note`, `Choice`, and `WeightedChoice` were not reachable from any real
document shape before this fixture set was written (nothing in
`test-specsheets/` embedded them) - `tasks/WidgetOptions` gained an
optional `notes` array and `tasks/FancyWidget` gained an optional
`choices` dict specifically so every rule has at least one legitimate
path to it from a real `TestDocument`.

Three `pass-*` fixtures round out the set: a minimal valid document, a
fuller one exercising every composition pattern at once (both widget
branches, both choice branches, namespace-free), and one with the
`acme` namespace registered (its `new/` class and its `updated/`
fragment on `SimpleWidget`, both valid). Two fixtures chain multiple
violations in one document to demonstrate that part of the naming
convention: one chains two different single-fire rules, the other
chains a rule that fires twice with one that fires once.

These fixtures were verified against a throwaway resolver script (not
checked in) that flattens `test-specsheets/`'s cross-file mixin
composition and generated `oneOf` discriminators by hand and re-derives
each fixture's expected rule ID(s) via Design.md's own Schema-Pass
Errors algorithm - the same kind of check the real generator will
eventually do automatically. It is not a substitute for the generator's
own test harness once that exists, which is what these fixtures are
ultimately for.
