package org.sedml.libsed2;

import java.util.List;

/** Read-only, type-erased view of an ID-keyed collection field (a "dict" of
 * elements or an "any-dict" of raw JSON values), so reference resolution
 * (References.getSedReference) can walk any class's containment tree
 * generically. GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public interface IdCollection {
    List<String> ids();

    boolean has(String itemId);

    /** The entry stored under itemId: a SedBase element for a "dict"
     * collection, a raw JsonNode for an "any-dict" one. */
    Object getObject(String itemId);
}
