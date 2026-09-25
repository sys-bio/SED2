---
id: SEDBase-0005
rule: "The first segment of a reference must name one of SEDDocument's ID-keyed collections: tasks, constants, outputs, or styles."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' starts with an unknown collection; it must start with #tasks, #constants, #outputs, or #styles."
severity: error
status: active
---

Applies to every reference anywhere in the document: a whole attribute value,
an element of an array or object value, or a REFERENCE token embedded in a
math string (see Types-0001). Owned by SEDBase rather than repeated on
every class, since every class can hold references; {class} in the message
names the element that holds the reference, not SEDBase.

Listing #outputs as a legal root keeps this rule purely syntactic;
SEDBase-0007 is the rule that rejects actually using it.
