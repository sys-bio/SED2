---
id: SEDDocument-0012
rule: "No JSON object in a SED2 document may contain the same key more than once."
message: "Key '{attr}' appears more than once at '{location}'."
severity: error
status: active
check: handwritten
---

JSON parsers silently keep one copy of a duplicated key (usually the last),
so a document with two tasks named sim1 would lose one without any error.
Catching this needs a parser-level hook in each language rather than
ordinary schema/tree-walk validation, since the duplicate is already gone
by the time normal parsing completes: Python's object_pairs_hook,
Jackson's STRICT_DUPLICATE_DETECTION (which throws and halts the parse,
rather than collecting alongside other errors the way every other rule
does), and a custom cursor-level handler for jsoncons in C++ (which has
no built-in duplicate-key option).

Decided not to implement detection for this rule in v1 - a genuinely
custom, per-language parser-level detector isn't worth the engineering
cost for what's expected to be a rare, hand-editing-only mistake. A
document with a duplicate key silently keeps whichever value the
underlying parser resolves to, with no error reported, in all three
languages. Because of this, no fixture should chain this rule onto
another rule's filename the way Testing otherwise allows - see Testing.
