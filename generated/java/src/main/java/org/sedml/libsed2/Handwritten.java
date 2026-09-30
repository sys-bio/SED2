package org.sedml.libsed2;

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

    public static final boolean HAS_REFERENCE_RULES = true;   // SEDBase-0005, SEDBase-0006, SEDBase-0007
    public static final boolean HAS_SHAPE_RULES = true;   // SEDBase-0008, SEDBase-0009, SEDBase-0010, SEDBase-0011, SEDBase-0012, SEDBase-0014, SEDBase-0015
    public static final boolean HAS_REF_TARGET_RULES = true;   // SEDBase-0016, SEDBase-0017
    public static final boolean HAS_SCOPING_RULES = true;   // SEDBase-0013
    public static final boolean HAS_TASK_ORDER_RULE = true;   // AbstractTask-0003
    public static final boolean HAS_REPEAT_OWN_RULES = true;   // Repeat-0008, Repeat-0009, Repeat-0010
    public static final boolean HAS_LOOPVAR_RULE = true;   // LoopVariable-0004
    public static final boolean HAS_NAMESPACE_RULES = true;   // SEDDocument-0009, SEDDocument-0010, SEDDocument-0011
    public static final boolean HAS_CONSTANTS_ORDER_RULE = true;   // SEDDocument-0013

    /** SEDBase-0005. */
    public static List<ValidationProblem> sedBase0005(ParsedReference parsed, String className, String idValue, String attr, String location) {
        return SedBase0005.check(parsed, className, idValue, attr, location);
    }

    /** SEDBase-0006. */
    public static List<ValidationProblem> sedBase0006(ParsedReference parsed, Object resolved, String resolvedPrefix, String className, String idValue, String attr, String location) {
        return SedBase0006.check(parsed, resolved, resolvedPrefix, className, idValue, attr, location);
    }

    /** SEDBase-0007. */
    public static List<ValidationProblem> sedBase0007(ParsedReference parsed, String className, String idValue, String attr, String location) {
        return SedBase0007.check(parsed, className, idValue, attr, location);
    }

    /** SEDBase-0008. */
    public static List<ValidationProblem> sedBase0008(Boolean accessorOk, String dotName, String value, String className, String idValue, String attr, String location) {
        return SedBase0008.check(accessorOk, dotName, value, className, idValue, attr, location);
    }

    /** SEDBase-0009. */
    public static List<ValidationProblem> sedBase0009(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return SedBase0009.check(dimsBefore, indexAccessors, value, className, idValue, attr, location);
    }

    /** SEDBase-0010. */
    public static List<ValidationProblem> sedBase0010(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return SedBase0010.check(dimsBefore, indexAccessors, value, className, idValue, attr, location);
    }

    /** SEDBase-0011. */
    public static List<ValidationProblem> sedBase0011(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return SedBase0011.check(dimsBefore, indexAccessors, value, className, idValue, attr, location);
    }

    /** SEDBase-0012. */
    public static List<ValidationProblem> sedBase0012(boolean ok, String badSubvalue, String resolvedValue, String value, String className, String idValue, String attr, String location) {
        return SedBase0012.check(ok, badSubvalue, resolvedValue, value, className, idValue, attr, location);
    }

    /** SEDBase-0013. */
    public static List<ValidationProblem> sedBase0013(boolean inScope, String targetRepeatId, String value, String className, String idValue, String location) {
        return SedBase0013.check(inScope, targetRepeatId, value, className, idValue, location);
    }

    /** SEDBase-0014. */
    public static List<ValidationProblem> sedBase0014(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value, String className, String idValue, String attr, String location) {
        return SedBase0014.check(dimsBefore, indexAccessors, value, className, idValue, attr, location);
    }

    /** SEDBase-0015. */
    public static List<ValidationProblem> sedBase0015(List<Dim> dimsAfter, String expectedType, String value, String className, String idValue, String attr, String location) {
        return SedBase0015.check(dimsAfter, expectedType, value, className, idValue, attr, location);
    }

    /** SEDBase-0016. */
    public static List<ValidationProblem> sedBase0016(String resolvedKind, String resolvedDescription, String value, String className, String idValue, String attr, String location) {
        return SedBase0016.check(resolvedKind, resolvedDescription, value, className, idValue, attr, location);
    }

    /** SEDBase-0017. */
    public static List<ValidationProblem> sedBase0017(String resolvedKind, String resolvedDescription, String value, String className, String idValue, String attr, String location) {
        return SedBase0017.check(resolvedKind, resolvedDescription, value, className, idValue, attr, location);
    }

    /** SEDDocument-0009. */
    public static List<ValidationProblem> sedDocument0009(String prefix, String location) {
        return SedDocument0009.check(prefix, location);
    }

    /** SEDDocument-0010. */
    public static List<ValidationProblem> sedDocument0010(String prefix, String location) {
        return SedDocument0010.check(prefix, location);
    }

    /** SEDDocument-0011. */
    public static List<ValidationProblem> sedDocument0011(SedBase document) {
        return SedDocument0011.check(document);
    }

    /** SEDDocument-0013. */
    public static List<ValidationProblem> sedDocument0013(IdCollection constants) {
        return SedDocument0013.check(constants);
    }

    /** AbstractTask-0003. */
    public static List<ValidationProblem> abstractTask0003(boolean ok, String value, String className, String idValue, String attr, String location) {
        return AbstractTask0003.check(ok, value, className, idValue, attr, location);
    }

    /** Repeat-0008. */
    public static List<ValidationProblem> repeat0008(boolean ok, Object value, String className, String idValue, String attr, String location) {
        return Repeat0008.check(ok, value, className, idValue, attr, location);
    }

    /** Repeat-0009. */
    public static List<ValidationProblem> repeat0009(boolean ok, Object value, String className, String idValue, String attr, String location) {
        return Repeat0009.check(ok, value, className, idValue, attr, location);
    }

    /** Repeat-0010. */
    public static List<ValidationProblem> repeat0010(boolean definesAppliedDimensions, Object value, String className, String idValue, String attr, String location) {
        return Repeat0010.check(definesAppliedDimensions, value, className, idValue, attr, location);
    }

    /** LoopVariable-0004. */
    public static List<ValidationProblem> loopVariable0004(boolean ok, Object value, String idValue, String location) {
        return LoopVariable0004.check(ok, value, idValue, location);
    }

}
