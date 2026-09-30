package org.sed2test;

import java.util.List;

/** A parsed reference string: '#' + colon-delimited containment path +
 * an optional chain of dot-accessors / bracket indices, e.g.
 * "#tasks:loop1:subTasks:sim1.model['S1']" (see References.parse). Pure
 * syntax - never touches a document. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class ParsedReference {
    /** One accessor: either a dot-accessor (name) or a bracket index. */
    public static final class Accessor {
        public final String dotName;    // non-null for a dot-accessor
        public final RefIndex index;    // non-null for a bracket index

        public Accessor(String dotName, RefIndex index) {
            this.dotName = dotName;
            this.index = index;
        }

        public boolean isDot() { return dotName != null; }
    }

    public final String raw;
    public final String collection;        // the segment right after '#', or null if empty
    public final List<String> path;        // colon-segments after the collection
    public final List<Accessor> accessors;

    public ParsedReference(String raw, String collection, List<String> path, List<Accessor> accessors) {
        this.raw = raw;
        this.collection = collection;
        this.path = path;
        this.accessors = accessors;
    }

    /** The first dot-accessor's name, or null. */
    public String firstDotName() {
        for (Accessor a : accessors) if (a.isDot()) return a.dotName;
        return null;
    }

    /** Every bracket index, in order, wherever it fell relative to a dot. */
    public List<RefIndex> indexAccessors() {
        List<RefIndex> out = new java.util.ArrayList<>();
        for (Accessor a : accessors) if (!a.isDot()) out.add(a.index);
        return out;
    }
}
