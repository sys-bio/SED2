'use strict';
// Hand-written JavaScript wrapper around the Emscripten module (sed2test.js,
// built from the C++ library by generated/js's CMakeLists.txt). Copied to
// <out>/js/index.js by generator/emit_js.py with the module's file name
// rewritten to match --cpp-namespace. It is the analog of libantimonyjs's
// scripts/ wrapper: it hides the cwrap/malloc plumbing behind plain methods.
//
//   const { load } = require('PACKAGE');
//   const sed2 = await load();
//   const result = sed2.validate(documentText);   // {ok, problems} | {ok:false, error}
//
// In a browser, include sed2test.js (the single-file build, WebAssembly
// embedded) and this file with <script> tags; both define globals, then
//   const sed2 = sed2Wrap(await sed2test());

const FUNCTIONS = [
  'sed2_library_version',
  'sed2_document_version',
  'sed2_class_names',
  'sed2_direct_only_keys',
  'sed2_rule_catalog',
  'sed2_validate_document',
  'sed2_validate_object',
  'sed2_normalize_document',
  'sed2_check_math',
];

/** Wraps an instantiated Emscripten module (the resolved value of the factory). */
function wrap(Module) {
  // Strings go through malloc rather than ccall's stack allocation, so a
  // large document cannot overflow the (small) WebAssembly stack.
  function call(name, ...args) {
    const ptrs = [];
    try {
      const cargs = args.map((s) => {
        const n = Module.lengthBytesUTF8(s) + 1;
        const p = Module._malloc(n);
        ptrs.push(p);
        Module.stringToUTF8(s, p, n);
        return p;
      });
      return Module.UTF8ToString(Module['_' + name](...cargs));
    } finally {
      ptrs.forEach((p) => Module._free(p));
    }
  }
  const json = (name, ...args) => JSON.parse(call(name, ...args));
  for (const name of FUNCTIONS) {
    if (typeof Module['_' + name] !== 'function') throw new Error('module does not export _' + name);
  }
  return {
    /** Version of this library (VERSION.txt at build time). */
    version: () => call('sed2_library_version'),
    /** Newest SED2 document-format version this library knows (e.g. "v1.0.0"). */
    documentVersion: () => call('sed2_document_version'),
    /** Names of every generated class. */
    classNames: () => json('sed2_class_names'),
    /** Keys accepted by validateObject(): the classes validated on their own, not inside a document. */
    directOnlyKeys: () => json('sed2_direct_only_keys'),
    /** {RuleID: {rule, message, severity}} for every validation rule. */
    ruleCatalog: () => json('sed2_rule_catalog'),
    /** Parse and validate a SED2 document: {ok:true, problems:[...]} or {ok:false, error}. */
    validate: (text) => json('sed2_validate_document', text),
    /** Validate one direct-only class instance, selected by a key from directOnlyKeys(). */
    validateObject: (key, text) => json('sed2_validate_object', key, text),
    /** Parse a document and write it back out in canonical form: {ok:true, text} or {ok:false, error}. */
    normalize: (text) => json('sed2_normalize_document', text),
    /** Syntax-check a SED2 math string: {ok:true} or {ok:false, error}. */
    checkMath: (text) => json('sed2_check_math', text),
  };
}

/** Loads the module (Node) and wraps it. modulePath defaults to the sibling build output. */
async function load(modulePath) {
  const factory = require(modulePath || './sed2test.js');
  return wrap(await factory());
}

if (typeof module !== 'undefined' && module.exports) module.exports = { wrap, load };
else if (typeof globalThis !== 'undefined') globalThis.sed2Wrap = wrap;
