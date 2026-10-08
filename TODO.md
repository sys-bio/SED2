# SED2 TODO

Design questions that need real thought before the specification can be finalized.

## ModelChange: addElements and replaceElements (and the order of changes)

Raised while building pySED2Translate (see its GAPS.md, S-010).

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
