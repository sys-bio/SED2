package org.sedml.libsed2;

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

    public FieldSpec(String name, String kind, boolean required, String ruleId, String requiredRuleId,
                      String originCatchall, Double minimum, Double exclusiveMinimum, String pattern,
                      String itemClass, String itemDiscriminator, boolean isMath) {
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
    }
}
