package org.sed2test;

import java.util.ArrayList;
import java.util.List;

/** Backing store for a plain (non-ID-keyed) array-of-embedded-object
 * field, e.g. WidgetOptions.notes: add- (append), remove- (by index),
 * insert- (at index). GENERATED - do not hand-edit. */
public final class ListCollection<T extends SedBase> {
    private final List<T> items = new ArrayList<>();

    public List<T> items() { return new ArrayList<>(items); }

    public void add(T obj) { items.add(obj); }

    public void insert(int index, T obj) {
        if (index < 0 || index > items.size()) throw new ApiError("index " + index + " out of range");
        items.add(index, obj);
    }

    public void remove(int index) {
        if (index < 0 || index >= items.size()) throw new ApiError("index " + index + " out of range");
        items.remove(index);
    }

    public int size() { return items.size(); }
}
