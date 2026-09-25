---
id: SEDDocument-0009
rule: "For every namespace prefix used anywhere in the document, SEDDocument must declare a <prefix>@version attribute."
message: "Namespace '{prefix}' is used at '{location}', but the document does not declare '{prefix}@version'."
severity: error
status: active
---

Applies to registered and unregistered prefixes alike: 'used' means any
attribute key or _type value of the form prefix@identifier, anywhere in the
document. The <prefix>@version attribute itself does not count as a use.
The version's format (v#.#.#) is a generated schema pattern for a registered
prefix (see Design.md's Namespaces section); for an unregistered prefix,
SEDDocument-0014 checks it by hand instead.
