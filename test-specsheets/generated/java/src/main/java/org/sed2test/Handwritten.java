package org.sed2test;

import java.util.ArrayList;
import java.util.List;

/** Facade over the hand-written per-rule check() classes (templates/java/rules/),
 * one static method per implemented rule with the same signature as the rule's own
 * check() - or, for a rule this spec tree does not define, the same signature as a
 * no-op - plus the HAS_* group flags References.java's dispatchers consult (the Java
 * analog of emit_python.py's ImportError guards). GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class Handwritten {
    private Handwritten() {}

    public static final boolean HAS_REFERENCE_RULES = false;   // SEDBase-0005, SEDBase-0006, SEDBase-0007
    public static final boolean HAS_SHAPE_RULES = false;   // SEDBase-0008, SEDBase-0009, SEDBase-0010, SEDBase-0011, SEDBase-0012, SEDBase-0014, SEDBase-0015
    public static final boolean HAS_REF_TARGET_RULES = false;   // SEDBase-0016, SEDBase-0017
    public static final boolean HAS_SCOPING_RULES = false;   // SEDBase-0013
    public static final boolean HAS_TASK_ORDER_RULE = false;   // AbstractTask-0003
    public static final boolean HAS_REPEAT_OWN_RULES = false;   // Repeat-0008, Repeat-0009, Repeat-0010
    public static final boolean HAS_LOOPVAR_RULE = false;   // LoopVariable-0004
    public static final boolean HAS_PARAMETER_SCAN_RULE = false;   // ParameterScan-0007
    public static final boolean HAS_NAMESPACE_RULES = false;   // SEDDocument-0009, SEDDocument-0010, SEDDocument-0011
    public static final boolean HAS_CONSTANTS_ORDER_RULE = false;   // SEDDocument-0013

    /** SEDBase-0005. */
    public static List<ValidationProblem> sedBase0005(ParsedReference parsed, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0006. */
    public static List<ValidationProblem> sedBase0006(ParsedReference parsed, Object resolved, String resolvedPrefix, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0007. */
    public static List<ValidationProblem> sedBase0007(ParsedReference parsed, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0008. */
    public static List<ValidationProblem> sedBase0008(Boolean accessorOk, String dotName, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0009. */
    public static List<ValidationProblem> sedBase0009(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0010. */
    public static List<ValidationProblem> sedBase0010(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0011. */
    public static List<ValidationProblem> sedBase0011(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0012. */
    public static List<ValidationProblem> sedBase0012(boolean ok, String badSubvalue, String resolvedValue, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0013. */
    public static List<ValidationProblem> sedBase0013(boolean inScope, String targetRepeatId, String value, String className, String idValue, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0014. */
    public static List<ValidationProblem> sedBase0014(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0015. */
    public static List<ValidationProblem> sedBase0015(List<Dim> dimsAfter, String expectedType, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0016. */
    public static List<ValidationProblem> sedBase0016(String resolvedKind, String resolvedDescription, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDBase-0017. */
    public static List<ValidationProblem> sedBase0017(String resolvedKind, String resolvedDescription, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** SEDDocument-0009. */
    public static List<ValidationProblem> sedDocument0009(String prefix, String location) {
        return new ArrayList<>();
    }

    /** SEDDocument-0010. */
    public static List<ValidationProblem> sedDocument0010(String prefix, String location) {
        return new ArrayList<>();
    }

    /** SEDDocument-0011. */
    public static List<ValidationProblem> sedDocument0011(SedBase document) {
        return new ArrayList<>();
    }

    /** SEDDocument-0013. */
    public static List<ValidationProblem> sedDocument0013(IdCollection constants) {
        return new ArrayList<>();
    }

    /** AbstractTask-0003. */
    public static List<ValidationProblem> abstractTask0003(boolean ok, String value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** Repeat-0008. */
    public static List<ValidationProblem> repeat0008(boolean ok, Object value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** Repeat-0009. */
    public static List<ValidationProblem> repeat0009(boolean ok, Object value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** Repeat-0010. */
    public static List<ValidationProblem> repeat0010(boolean definesAppliedDimensions, Object value, String className, String idValue, String attr, String location) {
        return new ArrayList<>();
    }

    /** LoopVariable-0004. */
    public static List<ValidationProblem> loopVariable0004(boolean ok, Object value, String idValue, String location) {
        return new ArrayList<>();
    }

    /** ParameterScan-0007. */
    public static List<ValidationProblem> parameterScan0007(List<String> modelElements, String className, String idValue, String location) {
        return new ArrayList<>();
    }

}
