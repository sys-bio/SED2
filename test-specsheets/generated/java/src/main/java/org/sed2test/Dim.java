package org.sed2test;

import java.util.List;
import java.util.Objects;

/** One statically-resolved dimension of a task output's shape (see
 * OutputsShape.resolveDims): its size and labels when known, and where
 * that knowledge comes from. GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class Dim {
    public final Long size;             // null when not statically known
    public final List<String> labels;   // null when not statically known
    public final String source;         // "static" | "input-file" | "runtime" | null
    public final Long min;              // guaranteed minimum size, or null

    public Dim(Long size, List<String> labels, String source, Long min) {
        this.size = size;
        this.labels = labels;
        this.source = source;
        this.min = min;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Dim)) return false;
        Dim d = (Dim) o;
        return Objects.equals(size, d.size) && Objects.equals(labels, d.labels)
                && Objects.equals(source, d.source) && Objects.equals(min, d.min);
    }

    @Override
    public int hashCode() { return Objects.hash(size, labels, source, min); }
}
