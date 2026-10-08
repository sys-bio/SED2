# Model formats

SED2 can refer to the current numerical value of an element of a model by
label, e.g. `#tasks:mod1.model["S1"]` (see "Elements of models" in
`specsheets/core/Types/v1.0.0/description.md`).  What a label may name, and
whether numerical indexing is meaningful at all, depends on the model format,
so each supported format gets its own directory here.

This directory is deliberately outside `specsheets/`: that tree holds class
data sheets, and a model format is not a SED2 class.

## Layout

    model_formats/
      <Format>/
        description.md      what the format is, its language URN(s), and an
                            index of the topic files below
        labels.md           namespaces, and what a label or index on .model
                            may refer to
        setValues.md        keys accepted in a ModelChange's setValues
        modelChange.md      addElements / removeElements / replaceElements
        elementTypes.md     ModelElementList includeTypes/excludeTypes
                            vocabulary
        validation/         one .md file per rule, same shape as the rules in
                            specsheets/<group>/<Class>/v1.0.0/validation/
        <Version>/          optional; only when a format's rules differ between
                            levels/versions (same layout as above)

Rule files use the same frontmatter as other SED2 rules (`id`, `rule`,
`message`, `severity`, `status`, `check`).  Rule ids are `<Format>-NNNN`.

Every format uses the same topic filenames, so formats can be compared side
by side.  A topic that has not been decided says "To be determined"; until it
is filled in, validation must assume that anything is potentially valid.  Add
a new topic file (and a row in the format's `description.md`) when a new
format-specific question comes up.

## Status

Everything here is `status: proposed` and `check: handwritten`: a format-aware
library implements these checks, and the generic validator does not.  Without
format information (an unknown `language`, or no format-aware library
available), validation must assume that any indexing scheme on `.model` is
potentially valid.
