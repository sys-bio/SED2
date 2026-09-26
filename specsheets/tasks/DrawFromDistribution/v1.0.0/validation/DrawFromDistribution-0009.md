---
id: DrawFromDistribution-0009
rule: When the value of distribution of a DrawFromDistribution is a reference, it must be a reference to one of the SBML distrib package's definitionURL values.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not one of the allowed distribution URIs ({allowed})."
severity: error
status: active
check: ref-type
---

`distribution` is `DistributionURI | SIdRef`: when the value is a reference, it must resolve to one of the 12 allowed distribution URIs.
