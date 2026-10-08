package org.sed2test;

import java.math.BigInteger;

/** One bracket index of a reference: [n] / [-n] ("int"), ['label'] ("label")
 * or [a:b] ("range", either end optional). GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class RefIndex {
    public final String kind;       // "int" | "label" | "range"
    public final long intValue;     // "int": the index (saturated to the long range)
    public final String intText;    // "int": the index as Python would print it
    public final String label;      // "label": the label
    public final Long rangeStart;   // "range": start (saturated to the long range), or null when open
    public final Long rangeEnd;     // "range": end (saturated to the long range), or null when open
    public final String rangeStartText;   // "range": the start as Python would print it, or null when open
    public final String rangeEndText;     // "range": the end as Python would print it, or null when open
    /** True when this index was written after a comma inside the same pair of
     * brackets as the previous index: "[0:2, 1]" is two indices, the second
     * flagged sameBracket. Separate brackets ("[0:2][1]") chain - each
     * bracket indexes the result of the one before - while the indices of one
     * bracket apply to consecutive dimensions of the value they start from,
     * like numpy's x[0:2, 1]. */
    public final boolean sameBracket;

    private RefIndex(RefIndex o, boolean sameBracket) {
        this.kind = o.kind;
        this.intValue = o.intValue;
        this.intText = o.intText;
        this.label = o.label;
        this.rangeStart = o.rangeStart;
        this.rangeEnd = o.rangeEnd;
        this.rangeStartText = o.rangeStartText;
        this.rangeEndText = o.rangeEndText;
        this.sameBracket = sameBracket;
    }

    /** A copy of this index with its sameBracket flag set as given. */
    public RefIndex withSameBracket(boolean sameBracket) {
        return new RefIndex(this, sameBracket);
    }

    private RefIndex(String kind, long intValue, String intText, String label, BigInteger rangeStart,
                     BigInteger rangeEnd) {
        this.kind = kind;
        this.intValue = intValue;
        this.intText = intText;
        this.label = label;
        this.rangeStart = rangeStart == null ? null : Long.valueOf(saturate(rangeStart));
        this.rangeEnd = rangeEnd == null ? null : Long.valueOf(saturate(rangeEnd));
        this.rangeStartText = rangeStart == null ? null : rangeStart.toString();
        this.rangeEndText = rangeEnd == null ? null : rangeEnd.toString();
        this.sameBracket = false;
    }

    public static RefIndex ofInt(BigInteger v) {
        return new RefIndex("int", saturate(v), v.toString(), null, null, null);
    }

    public static RefIndex ofLabel(String label) {
        return new RefIndex("label", 0, null, label, null, null);
    }

    public static RefIndex ofRange(BigInteger a, BigInteger b) {
        return new RefIndex("range", 0, null, null, a, b);
    }

    public static long saturate(BigInteger v) {
        if (v.bitLength() < 64) return v.longValue();
        return v.signum() < 0 ? Long.MIN_VALUE : Long.MAX_VALUE;
    }

    /** The index value as the reference rules print it in a message's
     * {subvalue} (the label itself, or the integer). */
    public String valueText() {
        if (kind.equals("int")) return intText;
        if (kind.equals("label")) return label;
        return rangeText();
    }

    /** "[a:b]" with an open end left empty. */
    public String rangeText() {
        return "[" + (rangeStartText == null ? "" : rangeStartText) + ":"
                + (rangeEndText == null ? "" : rangeEndText) + "]";
    }
}
