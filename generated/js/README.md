# libsed2js 0.1.1

The libsed2 C++ library (reading and validating SED2 documents), compiled to
WebAssembly with Emscripten. One self-contained module: the WebAssembly is
embedded in `libsed2.js`.

    const { load } = require("libsed2js");

    const sed2 = await load();
    const result = sed2.validate(documentText);
    if (!result.ok) console.error(result.error);          // not parseable
    else result.problems.forEach((p) => console.log(p.ruleId, p.location, p.message));

In a browser, include `libsed2.js` and `index.js` with script tags:

    const sed2 = sed2Wrap(await libsed2());

Methods: `version()`, `documentVersion()`, `classNames()`, `directOnlyKeys()`,
`ruleCatalog()`, `validate(text)`, `validateObject(key, text)`,
`normalize(text)`, `checkMath(text)`. See `index.d.ts`.
