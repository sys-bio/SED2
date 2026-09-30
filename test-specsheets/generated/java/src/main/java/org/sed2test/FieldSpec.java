package org.sed2test;

import java.util.List;

/** GENERATED - do not hand-edit; regenerate via generator/generate.py. */
public final class FieldSpec {
    public final String name;
    public final String kind;
    public final boolean required;
    public final String ruleId;            // nullable
    public final String requiredRuleId;    // nullable
    public final String originCatchall;
    public final Double minimum;           // nullable
    public final Double exclusiveMinimum;  // nullable
    public final String pattern;           // nullable
    public final String itemClass;         // nullable
    public final String itemDiscriminator; // nullable
    public final boolean isMath;           // x-math (Design.md's Math section / Types-0001..0004)
    public final Integer minLength;        // nullable (core/Types' URI leaf: "minLength": 1)
    public final List<String> enumValues;  // nullable: a fixed set of legal string values
    public final String refTypeRuleId;     // nullable: the formulaic "if a reference, must resolve to type X" rule
    public final String itemKind;          // nullable: ArrayOrRef element / DictOrRef value kind ("string" | "number" | "ref" | "any")
    public final String refTarget;         // nullable: x-ref-target ("model" -> SEDBase-0016, "annotatedData" -> SEDBase-0017)

    public FieldSpec(String name, String kind, boolean required, String ruleId, String requiredRuleId,
                      String originCatchall, Double minimum, Double exclusiveMinimum, String pattern,
                      String itemClass, String itemDiscriminator, boolean isMath, Integer minLength,
                      List<String> enumValues, String refTypeRuleId, String itemKind, String refTarget) {
        this.name = name;
        this.kind = kind;
        this.required = required;
        this.ruleId = ruleId;
        this.requiredRuleId = requiredRuleId;
        this.originCatchall = originCatchall;
        this.minimum = minimum;
        this.exclusiveMinimum = exclusiveMinimum;
        this.pattern = pattern;
        this.itemClass = itemClass;
        this.itemDiscriminator = itemDiscriminator;
        this.isMath = isMath;
        this.minLength = minLength;
        this.enumValues = enumValues;
        this.refTypeRuleId = refTypeRuleId;
        this.itemKind = itemKind;
        this.refTarget = refTarget;
    }
}
