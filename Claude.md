## Knowledge

You are an expert in Simulation Experiment Description languages.  The original was XML-based, and lives at C:\Users\Lucian\Desktop\sed-ml\specification\level-1-version-6\sed-ml-L1V6.pdf  The source of the new one is a series of markdown files in the root directory:  core-spec.md, and specsheets/.  It is in flux; you may propose changes to fix or resolve inconsistencies, but the user will have to make the changes himself.

The capabilities of that specification should persist in the new specification, but can take new forms.

The design of the new spec is that every element defines inputs and outputs, and can therefore be strung together in a Directed Acyclic Graph (DAG).

## Formatting

ASCII only, in all files. In particular, use a plain hyphen (-) instead of an em dash or en dash.

## Multi-Target Consistency

This project generates three separate libraries at once, in C++, Java, and Python (see Design.md).  Within a phase of work, Python may be designed and implemented first.  Its first pass must still add stubs for Java and C++ - raising or returning a clear not-yet-implemented error - so neither target is left silently absent.  Real Java and C++ implementations must land before that phase is merged.  Never merge a phase with only Python actually implemented.
