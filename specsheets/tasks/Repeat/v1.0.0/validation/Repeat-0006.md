---
id: Repeat-0006
rule: A Repeat must provide at least one of outputVariableMap or aggregateOutputVariables.
message: "{class} '{id}' must provide at least one of 'outputVariableMap' or 'aggregateOutputVariables'."
severity: error
status: active
check: schema
---

Repeat's schema expresses this as an `anyOf` of two single-field `required`
alternatives rather than a flat `required` list, since either field alone
satisfies it. See core-spec.md Section 8 for the `x-anyof-required-rule-id`
keyword that wires this rule to that `anyOf`.
