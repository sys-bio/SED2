'use strict';
// Hand-written glue: runs every fixture in this tree's fixtures/ directory
// through the JavaScript build of the library (the Emscripten output wrapped
// by ../index.js) and checks it against the rule ID(s)/count(s) encoded in
// the filename - see Design.md's Testing section for the naming convention.
// It mirrors templates/cpp/tests/FixtureTest.cpp (including the chain-suffix
// parsing rule: a rule ID's own trailing NNNN segment is always 4 digits,
// never a chain-count boundary), which this is the JavaScript analog of.
//
// Copied verbatim to <out>/js/test/fixtures.test.js by generator/emit_js.py.
// Run with Node's built-in runner, pointing LIBSED2_MODULE at the built
// single-file module:
//
//   LIBSED2_MODULE=/path/to/build/sed2test.js node --test test/fixtures.test.js
//
// SED2_FIXTURES_DIR overrides where fixtures/ is (default: three levels up
// from this file, i.e. <repo>/fixtures for <repo>/generated/js/test/).

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { load } = require('../index.js');

const FIXTURES_DIR = process.env.SED2_FIXTURES_DIR || path.join(__dirname, '..', '..', '..', 'fixtures');
const MODULE_PATH = process.env.LIBSED2_MODULE ? path.resolve(process.env.LIBSED2_MODULE) : undefined;

function fixtureFiles(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== 'archive') out.push(...fixtureFiles(p));
    } else if (entry.isFile() && entry.name.endsWith('.sed2.json')) {
      out.push(p);
    }
  }
  return out.sort();
}

const FIXTURE_RE = /^([A-Za-z0-9_-]+)-(pass|fail)-(\d+)-(.+?)((?:-[A-Za-z0-9_-]+-\d+)*)\.sed2\.json$/;

function expectedFromFilename(base) {
  if (base.startsWith('pass-')) return { kind: 'pass', rules: [] };
  const m = FIXTURE_RE.exec(base);
  assert.ok(m, `fixture name doesn't match convention: ${base}`);
  const rules = [[m[1], parseInt(m[3], 10)]];
  const chain = m[5].replace(/^-+/, '');
  if (chain) {
    const parts = chain.split('-');
    // Only a non-4-digit numeric token ends a chain segment.
    const nums = [];
    parts.forEach((p, i) => { if (/^\d+$/.test(p) && p.length !== 4) nums.push(i); });
    let start = 0;
    for (const idx of nums) {
      rules.push([parts.slice(start, idx).join('-'), parseInt(parts[idx], 10)]);
      start = idx + 1;
    }
  }
  return { kind: m[2], rules };
}

// Structural equality for the round-trip check: key order is not significant,
// numbers compare within Design.md's shared tolerance.
function jsonEqual(a, b) {
  if (typeof a === 'number' && typeof b === 'number') {
    return Math.abs(a - b) <= Math.max(1e-6 * Math.max(Math.abs(a), Math.abs(b)), 1e-12);
  }
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.length === b.length && a.every((x, i) => jsonEqual(x, b[i]));
  }
  if (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a) && !Array.isArray(b)) {
    const ka = Object.keys(a);
    return ka.length === Object.keys(b).length && ka.every((k) => Object.prototype.hasOwnProperty.call(b, k) && jsonEqual(a[k], b[k]));
  }
  return a === b;
}

const files = fixtureFiles(FIXTURES_DIR);

test('fixtures directory is populated', () => {
  assert.ok(files.length > 0, `no *.sed2.json fixtures under ${FIXTURES_DIR}`);
});

test('module reports its versions and rule catalog', async () => {
  const sed2 = await load(MODULE_PATH);
  assert.match(sed2.version(), /^\d+\.\d+\.\d+$/);
  assert.ok(sed2.classNames().includes('SEDDocument'));
  assert.ok(Object.keys(sed2.ruleCatalog()).length > 0);
});

let apiPromise;
const api = () => (apiPromise = apiPromise || load(MODULE_PATH));

for (const file of files) {
  const base = path.basename(file);
  test(path.relative(FIXTURES_DIR, file), async () => {
    const sed2 = await api();
    const expected = expectedFromFilename(base);
    const raw = fs.readFileSync(file, 'utf8');
    const primary = expected.rules.length ? expected.rules[0][0] : '';
    const direct = sed2.directOnlyKeys().includes(primary);

    const result = direct ? sed2.validateObject(primary, raw) : sed2.validate(raw);
    assert.strictEqual(result.ok, true, `${base}: ${result.error}`);
    const problems = result.problems;

    if (!direct && expected.kind === 'pass') {
      const rt = sed2.normalize(raw);
      assert.strictEqual(rt.ok, true, `${base}: ${rt.error}`);
      assert.ok(jsonEqual(JSON.parse(rt.text), JSON.parse(raw)), `round-trip mismatch for ${base}`);
    }

    if (expected.kind === 'pass') {
      assert.strictEqual(problems.length, 0, `${base} expected to pass, got ${JSON.stringify(problems.map((p) => p.ruleId))}`);
      return;
    }
    const counts = {};
    for (const p of problems) counts[p.ruleId] = (counts[p.ruleId] || 0) + 1;
    for (const [rid, n] of expected.rules) {
      assert.strictEqual(counts[rid] || 0, n, `${base}: expected rule ${rid} to fire ${n} time(s), got ${counts[rid] || 0}`);
    }
    const allowed = new Set(expected.rules.map((r) => r[0]));
    for (const rid of Object.keys(counts)) {
      assert.ok(allowed.has(rid), `${base}: unexpected extra violation ${rid} fired ${counts[rid]} time(s)`);
    }
  });
}
