---
id: SEDBase-0010
rule: "A label index in a reference must name one of the labels of the dimension it indexes."
message: "Reference '{value}' in attribute '{attr}' of {class} '{id}' uses label {subvalue}, which is not one of: {allowed}."
severity: error
status: active
---

Only fires when that dimension's labels are "static" in outputs.json and all
the fields they are computed from are literals. For example, with
outputVariables ["S1","S2"], '#tasks:sim1['S3']' fires this rule; with
outputVariables given as a reference, it cannot fire.
