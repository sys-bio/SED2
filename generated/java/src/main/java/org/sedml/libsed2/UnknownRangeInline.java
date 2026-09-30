package org.sedml.libsed2;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/** Opaque holder for a RangeInline instance whose _type names an
 * unregistered namespace prefix (see Design.md's Namespaces section) -
 * round-trips unchanged, never itself a validation error. GENERATED - do
 * not hand-edit; regenerate via generator/generate.py. */
public final class UnknownRangeInline extends SedBase {
    private final String typeValue;
    private final ObjectNode raw;

    public UnknownRangeInline(String typeValue, JsonNode raw) {
        this.typeValue = typeValue;
        this.raw = raw.deepCopy();
    }

    public String getType() { return typeValue; }

    @Override
    public String typeValue() { return typeValue; }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = raw.deepCopy();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        return d;
    }

    @Override
    public Set<String> allowedKeys() {
        Set<String> keys = new HashSet<>();
        raw.fieldNames().forEachRemaining(keys::add);
        return keys;
    }

    @Override
    protected List<ValidationProblem> validateOwn() {
        return new ArrayList<>();
    }
}
