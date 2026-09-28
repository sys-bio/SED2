package org.sed2test;

import java.util.HashMap;
import java.util.Map;

/** Rule catalogue + ValidationProblem factory. GENERATED (this file) - do
 * not hand-edit; regenerate via generator/generate.py. Populated by
 * RulesData at class-init time: ruleId -> (rule text, message template,
 * severity). Unlike the Python target's make_problem(), this takes an
 * explicit Map of placeholders rather than **kwargs, so there is no
 * possible collision with the `location` parameter - see this module's
 * docstring in generator/emit_java.py. */
public final class RuleCatalog {
    public static final class Entry {
        public final String rule;
        public final String messageTemplate;
        public final String severity;

        public Entry(String rule, String messageTemplate, String severity) {
            this.rule = rule;
            this.messageTemplate = messageTemplate;
            this.severity = severity;
        }
    }

    public static final Map<String, Entry> CATALOG = new HashMap<>();

    private RuleCatalog() {}

    public static Entry get(String ruleId) {
        Entry e = CATALOG.get(ruleId);
        return e != null ? e : new Entry("", "{schema-message}", "error");
    }

    public static String severityOf(String ruleId) {
        return get(ruleId).severity;
    }

    public static String formatMessage(String ruleId, String location, Map<String, Object> placeholders) {
        String out = get(ruleId).messageTemplate;
        out = out.replace("{location}", String.valueOf(location));
        for (Map.Entry<String, Object> e : placeholders.entrySet()) {
            out = out.replace("{" + e.getKey() + "}", String.valueOf(e.getValue()));
        }
        return out;
    }

    public static ValidationProblem makeProblem(String ruleId, String location, Map<String, Object> placeholders) {
        Entry e = get(ruleId);
        return new ValidationProblem(ruleId, e.severity, e.rule, formatMessage(ruleId, location, placeholders), location);
    }

    public static ValidationProblem makeProblem(String ruleId, String location) {
        return makeProblem(ruleId, location, new HashMap<>());
    }
}
