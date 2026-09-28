package org.sed2test;

/** GENERATED - do not hand-edit; regenerate via generator/generate.py. */
public final class ValidationProblem {
    public final String ruleId;
    public final String severity;
    public final String rule;
    public final String message;
    public final String location;

    public ValidationProblem(String ruleId, String severity, String rule, String message, String location) {
        this.ruleId = ruleId;
        this.severity = severity;
        this.rule = rule;
        this.message = message;
        this.location = location;
    }

    public String getRuleId() { return ruleId; }
    public String getSeverity() { return severity; }
    public String getRule() { return rule; }
    public String getMessage() { return message; }
    public String getLocation() { return location; }

    @Override
    public String toString() {
        return "ValidationProblem(" + ruleId + ", " + severity + ", " + location + ")";
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof ValidationProblem)) return false;
        ValidationProblem p = (ValidationProblem) o;
        return ruleId.equals(p.ruleId) && location.equals(p.location);
    }

    @Override
    public int hashCode() {
        return ruleId.hashCode() * 31 + location.hashCode();
    }
}
