"""ParameterScan-0007 (specsheets/tasks/ParameterScan/v1.0.0/validation/
ParameterScan-0007.md): "The entries of a ParameterScan's parameterRanges
must have pairwise distinct modelElement values." Each ParameterRange scans
one model element, and its modelElement also labels its entry in
[id].ranges and [id].indexes, so two entries with the same modelElement
would be ambiguous to address and redundant to scan. When modelElement is
given as a reference, entries are compared by the string it resolves to.

See templates/python/rules/Types-0001.py's module docstring for the shared
conventions (fixed `check` function name, no package-relative imports,
copied verbatim into every generated package's ._rules/ subpackage).
"""
from __future__ import annotations


def check(model_elements, *, class_name, id_value, location, make_problem):
    """The dispatcher (RUNTIME's _check_parameter_scan_ranges) has already
    reduced each entry of parameterRanges to its modelElement string, in
    order: the literal text, or the string a reference to a constant
    resolves to. An entry whose modelElement is missing, is not a string,
    or is a reference that does not resolve to a string is passed as None
    and ignored here (the schema and reference rules report those). One
    problem per distinct value that appears more than once, in order of
    first appearance, located at the second entry that has the value
    (<location>/<index>/modelElement; `location` is the parameterRanges
    list itself) so that two different duplicated values never share a
    location, which validate() would collapse into one problem. Comparison
    is exact (case-sensitive)."""
    seen = {}      # value -> number of entries seen so far
    problems = []
    for index, element in enumerate(model_elements):
        if element is None:
            continue
        seen[element] = seen.get(element, 0) + 1
        if seen[element] == 2:
            problems.append(make_problem(
                "ParameterScan-0007", f"{location}/{index}/modelElement", value=element,
                **{"class": class_name, "id": id_value}))
    return problems
