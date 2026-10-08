# SBML: ModelChange

How `addElements`, `removeElements` and `replaceElements` behave when the
model's language is SBML.

To be determined.

## addElements

To be determined.  Open: the syntax of the added string (the generic
description mentions an Antimony-formatted string; whether SBML fragments are
also allowed is not decided), and which element kinds may be added.

## removeElements

To be determined.  Open: which element kinds may be removed, and what happens
to elements that still refer to a removed one (for example a species used by
a reaction).

## replaceElements

To be determined.  The generic specification flags `replaceElements` as a
candidate for removal from SED2; fill this in only if it is kept.
