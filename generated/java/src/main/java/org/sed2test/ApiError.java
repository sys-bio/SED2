package org.sed2test;

/** Raised for any misuse of the generated API itself (wrong-kind OrRef
 * access, get on an unset field, an out-of-range insert, ...) - never for
 * a document that merely fails a SED2 validation rule. See Design.md's
 * Classes section. GENERATED - do not hand-edit. */
public class ApiError extends RuntimeException {
    public ApiError(String message) { super(message); }
}
