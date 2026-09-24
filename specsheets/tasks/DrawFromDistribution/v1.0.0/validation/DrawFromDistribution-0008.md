---
id: DrawFromDistribution-0008
rule: When the value of distribution of a DrawFromDistribution is provided directly, it must be one of the SBML distrib package's definitionURL values.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not one of the allowed distribution URIs ({allowed})."
severity: error
status: active
---

`distribution` is `DistributionURI | SIdRef`: the value, when not a reference, must be one of the 12 `http://www.sbml.org/sbml/symbols/distrib/*` URIs listed in `core/Types`'s `DistributionURI` (kept in sync with `schema/predefined-functions.json`'s `distrib` registry).
