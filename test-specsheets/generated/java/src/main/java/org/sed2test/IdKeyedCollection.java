package org.sed2test;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Backing store for an ID-keyed dict-of-discriminated-union field
 * (TestDocument.widgets/.reports, FancyWidget.choices) - insertion order
 * preserved, add-/remove-/insert-/rename (setId) per Design.md's Classes
 * section. Deliberately unbounded (not "T extends SedBase"): none of this
 * class's own methods call any SedBase-specific behavior, and an
 * "any-dict"-kind field (see generator/emit_java.py's emit_model_java_files)
 * reuses this same collection to hold raw JsonNode values instead of
 * SedBase instances - see generator/emit_python.py's _collection_accessors
 * any-dict branch for the reference implementation this mirrors.
 * GENERATED - do not hand-edit. */
public final class IdKeyedCollection<T> implements IdCollection {
    private final List<String> order = new ArrayList<>();
    private final Map<String, T> items = new LinkedHashMap<>();

    @Override
    public List<String> ids() { return new ArrayList<>(order); }

    @Override
    public boolean has(String itemId) { return items.containsKey(itemId); }

    @Override
    public Object getObject(String itemId) { return items.get(itemId); }

    public T get(String itemId) {
        if (!items.containsKey(itemId)) throw new ApiError("no entry with id " + itemId);
        return items.get(itemId);
    }

    public void add(String itemId, T obj) {
        if (items.containsKey(itemId)) throw new ApiError("an entry with id " + itemId + " already exists");
        order.add(itemId);
        items.put(itemId, obj);
    }

    public void insert(int index, String itemId, T obj) {
        if (items.containsKey(itemId)) throw new ApiError("an entry with id " + itemId + " already exists");
        if (index < 0 || index > order.size()) throw new ApiError("index " + index + " out of range");
        order.add(index, itemId);
        items.put(itemId, obj);
    }

    public void remove(String itemId) {
        if (!items.containsKey(itemId)) throw new ApiError("no entry with id " + itemId);
        order.remove(itemId);
        items.remove(itemId);
    }

    public void setId(String oldId, String newId) {
        if (!items.containsKey(oldId)) throw new ApiError("no entry with id " + oldId);
        if (items.containsKey(newId) && !newId.equals(oldId)) {
            throw new ApiError("an entry with id " + newId + " already exists");
        }
        int idx = order.indexOf(oldId);
        order.set(idx, newId);
        T v = items.remove(oldId);
        items.put(newId, v);
    }

    public int size() { return order.size(); }
}
