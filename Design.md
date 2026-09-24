## What is SED2?

SED stands for Simulation Experiment Description.  SED2 is a language for recording simulation experiments in JSON form that can be translated and exported to a number of different systems, where the core simulations and other analyses can be performed by a variety of tools.  It can be viewed as a generic workflow language, where instead of specific commands to a particular operating system and environment, it instead contains abstract commands that could be executed on a variety of operating systems and environments.

SED-ML was an earlier language (Simulation Experiment Description Markup Language), was XML-based, and tightly constrained.  The goal of SED2 is to change the format to JSON instead of XML, and expand the scope of what is possible to describe.

SED2 is designed to facilitate reproducibilty for the biological modeling community, much like SBML was desgned to facilitate model exchange for the biological modeling community.  In 20 years, the same SED2 document should be readable by a new library using new simulators and programs that don't exist today, and they should still produce the same results.

Ultimately, a SED2 'orchestrator' should be able to read a SED2 file, figure out who to ask to do each task, then stitch everything together to perform an efficient execution of all the tasks described in the document.

The SED2 specification originated as a Google Doc (with UML diagrams as Google Draw documents).  This monolithic document has since been split into `core-spec.md` - a short document describing the overall shape and design of a SED2 document - plus a `specsheets/` directory of per-class "Data Sheets," one per Task, Output, and supporting class, organized into `core/`, `tasks/`, `outputs/`, and `auxiliary/` categories. Each Data Sheet lives in its own versioned folder (`specsheets/<category>/<ClassName>/v1.0.0/`, with a change to that class getting a sibling folder named after the new document version - see Versioning) and contains a standalone, cross-referencing JSON Schema file, a UML diagram (or a `DIAGRAM-PENDING.md` placeholder where none exists yet - see `core-spec.md` Section 10 for the current list), and a `description.md` explaining what the class does and its attributes/outputs. **This split - `core-spec.md` plus `specsheets/` - is the canonical version of the spec.** Future spec changes should be made directly against `core-spec.md`/`specsheets/`.

## General Strategy

We want a code generator that produces three self-contained libraries - one each for C++, Java, and Python - that read and validate SED2 files, and can be used to create or otherwise manipulate a SED2 file.  Each generated library is a complete, independent codebase in its own language; none of them depend on each other or on the generator at runtime.  The SED2 design may change, and it definitely will expand with time, so the generator itself also needs to be flexibly changeable.

In a future project, we will use these libraries to write a translator of SED2 to a python script, a Julia script, and a Process Bigraph JSON file.  These libraries are constrained to serve as the base for those future translators.

## Testing

Everything should be test-driven.  We need tests for valid and invalid SED2 documents, and for each function (i.e. get/set), in each of the three generated libraries.  We will use each language's standard test framework: GoogleTest for C++, the same way that libantimony does (C:\Users\Lucian\Desktop\antimony); JUnit for Java; and pytest for Python.

This section covers document-level fixtures (fixtures/), which exercise the *generated libraries* - the same real specsheets/ classes a document author actually uses.  A separate, smaller fixture tree, test-specsheets/ (see Repository Layout), exercises the *generator itself*: one or two synthetic examples of each schema-composition pattern specsheets/ uses (the x-generated-oneOf discriminator, a directly-instantiable-and-subclassed Common mixin, a standalone schema-only mixin, a namespace new/ and updated/ example, and so on), kept deliberately small and stable so generator changes can be tested without depending on the size or churn of the real spec.  See test-specsheets/README.md for the full list of patterns it covers.

Document-level tests - valid and invalid SED2 documents, and the validation errors an invalid one is expected to produce - live in a single, language-independent directory of input files and expected outcomes.  This directory sits outside the per-language template and generated directories described under Code Generation below, and all three test suites read from it rather than keeping their own copies, so the three libraries can never drift out of sync on what counts as valid, or on what error a given invalid document should produce.

Fixture files are named after the validation rule(s) they exercise, adapted from the convention libSBML's test suite uses: `<rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>...].sed2.json` (see Repository Layout for the extension).  The leading rule ID identifies the constraint under test; `pass` or `fail` says whether the document should validate; `count` is how many times that rule is expected to fire (`00` for a pass case); and `test` distinguishes multiple fixtures for the same rule.  A document crafted to fail more than one rule at once chains additional `<rule-id>-<count>` pairs onto the end - for example `ExplicitODESimulation-0001-fail-01-02-BoundedODESimulation-0002-01` fails rule ExplicitODESimulation-0001 once and rule BoundedODESimulation-0002 once.  Unlike libSBML's convention, every chained rule carries its own count, not just the first, so a fixture can exercise interacting rules that each fire more than once.  Fail-case fixtures are checked against the specific rule IDs and counts encoded in the filename, not just a total error count, and each fail case should violate only the rule(s) named in its filename so that check stays meaningful.

Pass-case fixtures need no separate expected-output file: the check is that parsing and re-serializing reproduces the same document.  That comparison is done as JSON values - same keys, same values, same key order, checked recursively - rather than as literal text, since the three languages' serializers won't agree on whitespace or formatting.  Key order matters throughout, not just for `tasks`: SED2 relies on it so a naive executor can walk the document top-to-bottom without needing a value before it's produced, so round-tripping has to preserve it exactly (see JSON Libraries).

## Test Generation and Spec Evolution

Fixtures split into two tiers, maintained differently, so that spec changes don't force a wholesale revamp of the test suite.

Schema-derivable fixtures - for constraints the JSON schema captures directly, like required fields, types, enums, and patterns - are generated mechanically by the same generator run that produces the class code (see Code Generation below), into their own generated directory alongside it.  A required field implies a missing-it fixture; an enum implies one fixture per invalid value outside it; and so on.  These are never hand-edited and can't go stale: whenever the schema changes, they regenerate along with everything else.

Semantic fixtures - for the hand-written numbered rules described under Validation, such as cross-reference resolution, math well-formedness, and interactions between rules - stay hand-authored, since a machine has no way to know which cases are actually interesting to test.  To keep spec evolution from forcing these to be rewritten, rule numbers are append-only and never silently redefined: if an existing numbered rule's real behavior needs to change, that mints a new rule number and deprecates the old one, rather than editing the old number's meaning in place.  This append-only policy is enforced per class, inside that class's own validation/ folder (see Rule Documentation under Validation) rather than through any centralized registry.  A deprecated rule's fixtures move to an archive directory, kept for history but excluded from the active suite, rather than being deleted or rewritten.  Under this discipline, most spec growth - including behavioral changes, not just clean additions - becomes writing new fixtures for a new or superseded rule number, which is ordinary incremental work rather than a revamp.

The one case that legitimately requires editing an existing fixture is a genuine bug fix to a rule that was implemented incorrectly - normal, bounded maintenance, not something spec evolution should routinely cause.  CI running on every push (see CI below) is the backstop either way: a rule whose behavior quietly shifted shows up immediately as a named, specific failure - a rule number and test number - rather than silent drift discovered later.

Because the fixture directory is shared across all three generated languages (see Testing above), hand-authoring a semantic fixture is a cost paid once, not three times.

## CI

GitHub Actions runs the pipeline on every push, in two stages:

1. A single 'generate' job runs the code generator once and uploads the three generated-library directories (see Code Generation below) as build artifacts, so every language is built and tested against the exact same generator run rather than each regenerating independently.
2. A matrix job, one per language (C++, Java, Python), downloads its generated directory, compiles it, and then runs that language's test suite (GoogleTest, JUnit, pytest) against it, using the shared fixture directory described under Testing above.

Any job failing fails the whole run.  Because the matrix jobs are separate, a compile or test failure is attributed to the specific language and stage that broke, and a break in one target's generated code can't hide a break in another's.

## Repository Layout

```
SED2/
|-- Design.md
|-- Claude.md
|-- README.md
|-- LICENSE
|-- core-spec.md                     canonical spec: overall shape/design of a SED2 document
|-- specsheets/                      canonical per-class Data Sheets (schema + diagram + description)
|   |-- core/, tasks/, outputs/, auxiliary/
|   |   `-- <ClassName>/v1.0.0/      schema.json (+ inline./common.schema.json where merged), <ClassName>.png or DIAGRAM-PENDING.md, description.md, validation/*.md, outputs.json (tasks/ concrete classes only - see core-spec.md Section 8)
|-- test-specsheets/                 synthetic generator-test fixtures, same shape as specsheets/ + namespaces/ - see README.md there and Design.md's Testing section
|-- tools/
|   `-- build_specification.py       assembles core-spec.md + specsheets/ into SPECIFICATION.md on demand (see Specification Assembly)
|-- namespaces/                      known third-party namespace extensions, composed into the schema at generate time (see Namespaces)
|   `-- <prefix>/
|       |-- new/                     wholly new classes this namespace defines
|       |   `-- core/, tasks/, outputs/, auxiliary/
|       |       `-- <ClassName>/<namespace-version>/   schema.json, description.md, validation/*.md (IDs: <prefix>-<ClassName>-NNNN)
|       `-- updated/                 attributes this namespace adds to an existing class
|           `-- core/, tasks/, outputs/, auxiliary/
|               `-- <ClassName>/<namespace-version>/   schema.json, description.md, validation/*.md (IDs: <ClassName>-<prefix>-NNNN)
|-- schema/
|   |-- predefined-functions.json    math function/constant registry (MathML + distrib + SED2-specific)
|   `-- outputs-meta.schema.json   validates every tasks/ class's outputs.json envelope (see core-spec.md Section 8)
|-- generator/                       the generator's own hand-written source
|-- templates/
|   |-- cpp/                         hand-written C++-only code
|   |-- java/
|   |   `-- tests/                   hand-written JUnit fixture-harness glue
|   `-- python/
|       `-- tests/                   hand-written pytest fixture-harness glue
|-- generated/
|   |-- cpp/                         fully self-contained, generated C++ library
|   |-- java/
|   |-- python/
|   |-- schema/                      assembled 2020-12 schema tree: specsheets/ + registered namespaces/, composed (see Namespaces) - read directly by networknt/jsonschema, and the source for schema-draft7/
|   |-- schema-draft7/               generated draft-7 mirror of generated/schema/, for pboettch only (see JSON Libraries)
|   `-- rules-v*.json                one generated file per document version (see Rule Documentation)
|-- fixtures/
|   |-- generated/                   schema-derivable pass/fail fixtures, regenerated every run
|   |-- handwritten/                 semantic-rule fixtures, hand-authored
|   `-- archive/                     deprecated-rule fixtures, excluded from the active suite
`-- .github/
    `-- workflows/
        `-- ci.yml
```

Each `templates/<language>/` directory mirrors the internal path layout of its corresponding `generated/<language>/` directory, so the generator can merge template and generated content by relative path without a separate mapping file.

Fixture files use a `.sed2.json` extension - unambiguous as a SED2 document while every tool still treats it as JSON - rather than the bare `.sed2` extension the old prototype used.  A fixture's full filename is self-describing (see Testing), so no companion expected-output file is needed.

specsheets/ - plus any registered namespaces/ extensions (see Namespaces) - is the canonical source every piece reads.  The generator composes them at generate time into generated/schema/, the complete assembled 2020-12 schema tree that Java's networknt and Python's jsonschema load directly, since both support 2019-09/2020-12; C++'s pboettch instead reads generated/schema-draft7/, a further mechanical downgrade of generated/schema/ itself (see JSON Libraries), so a namespace's schema reaches all three validators exactly the way a built-in class's does.  Since none of the schema validators can map their own errors back to a rule number anyway (see Validation), the canonical schemas also carry generator-only metadata - subvariable lists, bare-reference legality, per-attribute rule IDs - as custom `x-`-prefixed keywords next to each constraint, which JSON Schema validators are required to ignore.  `schema/predefined-functions.json` stays separate, since it's a flat function/constant registry rather than an object-shape constraint - its own folder's fate (whether anything else still belongs alongside it under schema/) hasn't been revisited since specsheets/ took over the class schemas.

## Specification Assembly

core-spec.md and specsheets/ are split for authoring (see Repository Layout: a short document describing the overall shape plus one Data Sheet per class), but nothing stitches them back into a single document meant to be read end-to-end.  `tools/build_specification.py` does that: it discovers every class directly from specsheets/ - the same way the generator discovers AbstractTask/AbstractOutput branches (see Classes) - picking each class's highest version directory, and assembles core-spec.md's sections plus every class's description.md, diagram, and numbered validation rules into a single SPECIFICATION.md at the repository root.  Headings are shifted so the whole thing nests under one document outline, same-folder and cross-class links are rewritten to resolve from the repository root or to in-document anchors, and a table of contents is generated, so the result reads as one page on GitHub and also converts cleanly to HTML or PDF with pandoc.

SPECIFICATION.md is a generated file - never hand-edited, regenerated by re-running the script - and isn't checked into the repository or produced by CI (see CI); it's built on demand, whenever a single combined view of the spec is actually wanted.  Because the script discovers classes and versions straight from specsheets/ rather than from any hardcoded list, it keeps working as classes are added, renamed, split, or restructured, with no changes of its own required.  What can go stale, and needs hand-maintenance as the spec evolves, is anything the script assumes about shape rather than content - core-spec.md's section structure, the heading levels inside a description.md, validation/*.md's YAML-frontmatter-plus-prose format - so the script should be revisited whenever one of those conventions changes.

## Design

### Language Versions

* C++: C++17.
* Java: Java 21 (LTS).  Java 17 leaves premier support this year, and Java 21 has premier support into 2028 while still matching the modern (Java 17+) build of networknt/json-schema-validator.
* Python: Python 3.13 or later.

### JSON Libraries

Each generated library uses the JSON parser/DOM and JSON-schema validator most idiomatic for its language, chosen so the schema validator works directly against that language's own JSON tree, without a conversion step:

* C++: nlohmann::ordered_json (https://github.com/nlohmann/json) for the parser/DOM, paired with pboettch/json-schema-validator (https://github.com/pboettch/json-schema-validator) for the schema pass mentioned under Validation below.  nlohmann's types are header-only, MIT-licensed, require only C++11, and have strong MSVC support.  The ordered variant preserves object key order exactly as parsed, rather than sorting keys alphabetically the way the default nlohmann::json does - needed because SED2 relies on the order of entries like `tasks` being meaningful (see Testing).  Its dynamic tree is also what lets a namespace's opaque content round-trip unchanged when that namespace isn't registered (see Namespaces) - the schema validation pass still rejects a plain unrecognized field with no namespace at all; only namespace-prefixed content that no registered namespace claims gets this opaque treatment.  Building or looking up keys in a large ordered_json object is O(n^2) rather than O(log n), which is irrelevant at SED2 document sizes.  pboettch's API is hardcoded to the plain nlohmann::json type, not templated, so the schema pass runs against a throwaway plain-json copy of the document (order doesn't matter for that pass) rather than the ordered_json original.
* Java: Jackson's JsonNode tree model (jackson-databind) for the parser/DOM, paired with networknt/json-schema-validator (https://github.com/networknt/json-schema-validator), which validates directly against Jackson's JsonNode.  Both are Apache-2.0 and actively maintained; JsonNode holds the same kind of dynamic tree, for the same reason - namespace-opaque content, not general unrecognized-field tolerance.
* Python: the standard library's json module, which parses directly into native dicts/lists, so there's no separate DOM library to choose.  Paired with the jsonschema package (https://github.com/python-jsonschema/jsonschema, MIT-licensed), which validates those same native structures.

pboettch only supports JSON Schema draft 7, while networknt and jsonschema support 2019-09/2020-12.  Rather than constrain the canonical schemas to draft-7 features, the generator produces generated/schema-draft7/ as a mechanical downgrade of generated/schema/ itself (see Repository Layout) - the same assembled tree networknt and jsonschema read, with namespace composition already folded in, so the downgrade needs no namespace-specific logic of its own.  Every keyword the composed schemas actually use is already draft-7-compatible except $defs and unevaluatedProperties.  $defs is renamed to definitions (rewriting every #/$defs/X fragment inside a $ref to match), $schema is updated to the draft-07 URI, and each unevaluatedProperties: false class has its allOf-composed properties - including any contributed by a registered namespace's updated/ fragment (see Namespaces) - flattened into a local properties dict (as bare true placeholders - reconstructing what additionalProperties needs to see locally, the way every class's schema used to look before switching to unevaluatedProperties - see Classes) with unevaluatedProperties itself renamed to additionalProperties.  The same flattening covers patternProperties: SEDBaseFields's namespace catch-all (see Namespaces) is composed into every class via allOf, so it's copied down into each leaf's local schema alongside the flattened properties - draft 7's additionalProperties, unlike unevaluatedProperties, only sees patternProperties declared in its own schema object, not one reached through a composed-in $ref.  Because the mirror is generated fresh every run, it can't go stale the way a hand-maintained draft-7 copy would, and this keeps validation behavior equivalent across all three generated libraries without constraining how the canonical schemas are authored.

### Versioning

A SED2 document carries a single semantic version in SEDDocument's `version` attribute (e.g. "v1.0.0") - while the spec is pre-release this stays at "v1.0.0".  There is one version number for the whole document format, not one per class.  The attribute must match the pattern v#.#.# (major.minor.patch, with a leading v - the same shape as the version directory names below), enforced both as a JSON Schema pattern and as a validation rule (see SEDDocument's Data Sheet).

Whenever any class changes, the document version increments, but only the class(es) that actually changed get a new version directory under specsheets/<category>/<ClassName>/ - e.g. v1.0.1/ alongside the existing v1.0.0/.  A class that didn't change keeps using its existing directory; nothing forces every class to be re-published at every version bump.

To find the directory a class should use for a document declared at version vD, take that class's version directories and pick the highest one that is not greater than vD.  For example, if ExplicitODESimulation has directories v1.0.0/, v1.1.2/, and v1.2.2/, a document declared as v1.2.0 resolves to v1.1.2/ - the newest directory that isn't newer than the document itself.

Directory names are exact semver strings, not just a major number - v1.0.0/, not v1/ - since a class can gain a new directory at any version bump, not just a major one.

Namespaces carry their own, independent version numbers, unrelated to the document's own version - see Namespaces.

### Classes
Each SED2 class should have a corresponding class generated in each of the three target languages.  The classes are defined by the '_type' child, Each child attribute is owned by its parent, and should have get-, set- isSet- and unset- functions.  Each class will have a predefined list of child attributes, defined in the specification.

Some child objects themselves are lists, for example, the 'tasks' child of the document.  'getTasks', then should return an ordered list of tasks, with each task being its own subclass type, defined by its "_type" attribute.  List children need a list API, as well: add- (append at end), remove- (remove the child with the given ID), and insert- (place in list at given index).

Not every specsheets/ folder is a class, though.  specsheets/core/Types bundles the shared primitive and reference-helper types (SId, SIdRef, NumberOrRef, ScaleType, and so on) that every other Data Sheet's schema.json pulls in via $ref - it has no UML diagram, no _type discriminator, and is never itself instantiated as a document element.  The generator should treat it as a source of shared type definitions (mapping each $def to whatever the target language uses for that primitive or reference type - a typedef, a small wrapper/validation class, an enum, etc.), not as a class to generate get-/set-/isSet-/unset- accessors for.

AbstractTask's and AbstractOutput's _type discriminators are themselves entirely generated, not hand-maintained - and the mechanism needs no external list anywhere of which discriminators exist or which Common mixin each one scans for; it's self-describing from the files alone.  AbstractTask/v1.0.0/schema.json's $defs/AbstractTask entry carries no oneOf in its hand-authored form.  Instead it carries an x-generated-oneOf key whose value is a $ref-style pointer at its Common mixin (common.schema.json#/$defs/AbstractTaskCommon); AbstractOutput/v1.0.0/schema.json's $defs/AbstractOutput carries the same marker, pointing at AbstractOutputCommon.  To build a discriminator's oneOf, the generator: (1) finds every $defs entry across specsheets/ and registered namespaces that carries an x-generated-oneOf marker; (2) resolves that marker's pointer to find the discriminator's own Common schema; (3) scans every schema.json under specsheets/ - all four categories, since some concrete task types (Range, NumericRange, ParameterRange) live under auxiliary/ rather than tasks/ - for any class whose own allOf composes that same Common schema and pins a _type with const, and treats each match as a branch.  A class registers itself as a legal branch purely by declaring its own parentage via allOf; the discriminator is a computed view over that, never a separately hand-maintained list.  This is the same discovery rule namespace new/ classes already use (see Namespaces): adding a new built-in task or output type is exactly as lightweight as registering a namespace one - drop a new Data Sheet folder in the right place, and the generator picks it up, with no edit to AbstractTask's or AbstractOutput's own file ever required.  Because the x-generated-oneOf marker is itself how the generator finds discriminators to populate, introducing an entirely new abstract-class family - not just a new branch of an existing one - needs no generator code changes either: give it its own common.schema.json (say, FooCommon) and a schema.json whose $defs entry carries an x-generated-oneOf pointer at that Common schema, and the generator discovers and populates it the same way it does AbstractTask, AbstractOutput, and RangeInline.

RangeInline (specsheets/auxiliary/Range/v1.0.0/inline.schema.json) is a third instance of the exact same mechanism, at a narrower scope: its x-generated-oneOf marker points at RangeCommon (specsheets/auxiliary/Range/v1.0.0/common.schema.json), so the generator scans for classes whose own allOf composes RangeCommon and pins a _type const - currently Range, NumericRange, and ParameterRange.  RangeInline has to live in its own file/$defs entry rather than reusing Range's own schema.json the way AbstractTask reuses its own $defs/AbstractTask: Range, unlike AbstractTask, is itself directly instantiable (a bare Range with just values is a legal standalone task), so specsheets/auxiliary/Range/v1.0.0/schema.json's $defs/Range entry is already the concrete class, pinning _type const "range" - it can't simultaneously be the union placeholder.  Any future class that's both directly instantiable and the root of further subclasses needs this same split: its own common.schema.json for the shared mixin, plus a separate file for the generated union, rather than repurposing its own schema.json the way a never-instantiated abstract root can.

### Namespaces

SED2 documents may be extended by third parties with attributes or entirely new task/output types under a `namespace@identifier` syntax (see core-spec.md Section 5).  A namespace the generator doesn't know about is unaffected - its content round-trips unchanged, unvalidated, because it's still syntactically namespace-prefixed even though this particular prefix isn't one the generator recognizes.  A field or _type with no namespace at all never gets this treatment - that's always a plain validation failure, the same as any other unrecognized property (see Classes).

A namespace the generator does know about - a known namespace - gets its schema composed directly into the canonical schema tree at generate time, so its content validates exactly like any built-in attribute or class, through the same three validators, with no separate runtime code path.

Each known namespace carries its own semantic version, entirely independent of the document's own version (see Versioning) - a namespace's schema can evolve on its own timeline.  Whenever a document uses anything from a given namespace, anywhere, it must also carry a <prefix>@version attribute on SEDDocument itself (e.g. saurolab@version), naming the namespace version that document was written against - mirroring SEDDocument's own version attribute, one level down, including its format: a namespace version must also match the pattern v#.#.# (e.g. v1.0.0).  Since the generator declares <prefix>@version directly on SEDDocument's composed schema for every registered namespace, that format is enforced the same way SEDDocument's own version is, as a plain schema pattern on the generated property - only the requiredness ("must be present if the namespace is used") is a whole-document conditional a plain schema can't express, and stays a semantic Validation rule (see Rule Documentation).

Known namespaces live in a namespaces/<prefix>/ directory (see Repository Layout), structured exactly like specsheets/: two top-level directories, new/ and updated/, each split into tasks/, core/, outputs/, and auxiliary/ the same way specsheets/ is, and then <ClassName>/<namespace-version>/schema.json below that - for example namespaces/saurolab/new/tasks/FancyAnalysis27/v1.0.0/ for a wholly new task type, or namespaces/saurolab/updated/tasks/ExplicitODESimulation/v1.0.0/ for new attributes saurolab adds to the existing ExplicitODESimulation class.  The <namespace-version> directory name is that namespace's own version, unrelated to the document format's version, and follows the same v#.#.# format.

Each <ClassName>/<namespace-version>/ leaf gets the same contents as a specsheets/ Data Sheet, not just a schema.json - a description.md, and a validation/ folder.  Rule IDs there can't reuse the bare [ClassName]-NNNN scheme without risking collision with that same class name's own core rules (or another namespace's), and a bare namespace@identifier-style ID isn't filename-safe either, so namespace rule IDs are hyphenated instead: an updated/ class's rules are <ClassName>-<prefix>-NNNN (e.g. ExplicitODESimulation-saurolab-0001) - the core class name leads, since that's the "real", pre-existing class being extended - while a new/ class's rules are <prefix>-<ClassName>-NNNN (e.g. saurolab-FancyAnalysis27-0001) - the namespace leads, since the class itself has no core identity of its own.

new/ classes are found by the exact same scan that finds built-in branches (see Classes) - the generator doesn't treat namespaces/ and specsheets/ differently when building AbstractTask's/AbstractOutput's oneOf, it scans both trees (plus any --namespace-dir directories) for classes composing the relevant Common mixin with a _type const, whatever tree they live in; a new/ class's discovered _type is just <prefix>@<TypeName> instead of a bare built-in one.  updated/ classes compose their declared attributes (each namespace-prefixed, e.g. saurolab@thisFactor) directly into that specific existing class's own schema, via allOf, the same way the class's own inline schema already composes in.  Because these are literal, per-class property declarations rather than a blanket pattern, unevaluatedProperties: false rejects anything else automatically - so a namespace@key that a known namespace hasn't declared for that particular class is a real validation failure, with no extra generator logic needed for that case.

Mechanically, none of this happens by editing canonical files - not AbstractTask's/AbstractOutput's own oneOf (see Classes), and not an updated/ fragment's target class either: specsheets/tasks/ExplicitODESimulation/v1.0.0/schema.json can't carry a $ref to a namespace fragment it doesn't know exists, and shouldn't need hand-editing every time one is registered.  Instead, for an updated/ fragment, the generator assembles a third schema per affected class, e.g. {"allOf": [{"$ref": ".../specsheets/.../ExplicitODESimulation/v1.0.0/schema.json#/$defs/ExplicitODESimulation"}, {"$ref": ".../namespaces/saurolab/updated/.../ExplicitODESimulation/v1.0.0/schema.json#/$defs/ExplicitODESimulation"}], "unevaluatedProperties": false} - generated fresh each run from whatever's currently registered, the same way a new/ class becomes a generated oneOf branch rather than something hand-edited into AbstractTask/AbstractOutput.  This assembled tree is materialized as generated/schema/ (see Repository Layout): the complete, namespace-composed 2020-12 schema, which networknt and jsonschema load directly and which generated/schema-draft7/ is itself downgraded from (see JSON Libraries).  Both complete schemas - generated/schema/ and generated/schema-draft7/ - are generated outputs; specsheets/ and namespaces/ stay pure, hand-authored sources that never need editing just because a namespace gets registered.

Only a namespace prefix the generator has never heard of at all should be accepted as opaque, unvalidated passthrough.  That still needs a permissive catch-all: a generated patternProperties entry matching any prefix@identifier-shaped key except the prefixes currently registered (built fresh each generate run from namespaces/ plus any --namespace-dir directories - see below), so an unregistered prefix still passes through opaque while a wrong identifier under a registered prefix still fails.  Declared once, on SEDBaseFields (see core/SEDBase) - the same place name/description/notes/annotations are already centralized - it reaches every class through the allOf composition already in place; unevaluatedProperties is defined to see patternProperties evaluated anywhere in that composed tree, not just the local schema object, so this needs no extra logic for the 2020-12 schema Java and Python read directly.  The draft-7 mirror is the exception: draft 7's additionalProperties can't see a patternProperties reached through a composed-in $ref, so the downgrade script copies it down into each leaf's local schema as part of the same flattening step that already handles allOf-composed properties (see JSON Libraries).

Class-level types get the same "unregistered prefix is opaque, registered-but-wrong is an error" split, via a parallel fallback on the _type discriminator itself: a _type whose prefix isn't registered at all falls through to a generated UnknownClass - one per language, a minimal class that stores its contents as opaque literal values and returns its raw _type string from getType().  UnknownClass still subclasses AbstractTask or AbstractOutput, whichever discriminator it fell through, so it satisfies any code elsewhere that assumes its children are AbstractTask (or AbstractOutput) subclasses - for example Repeat's subTasks list.  A _type whose prefix is registered but whose identifier isn't one of that namespace's new/ classes does not fall through to UnknownClass - it's a real oneOf match failure, the same as the attribute-level case.  For now, referencing any namespaced task's output - whether it fell through to UnknownClass or resolved to a real generated new/ class - is limited to the same three forms any task supports: [id], [id].model, and [id].strings (see core-spec.md Section 4).  Nothing namespace-specific is reachable through a reference string, including a known namespace's own added attributes (from new/ or updated/ alike); this can be revisited later if it turns out people need deeper access.

The generator always composes whatever's in the repository's own namespaces/ directory.  To register a namespace without forking the project, the generator also accepts a repeatable --namespace-dir <path> flag pointing at additional directories in the same layout, composed the same way as the built-in ones.  A namespace prefix must be alphanumeric, and must not collide with any other currently-registered prefix.  By default, two sources defining the same prefix is an error ("namespace <prefix> defined twice") - the generator refuses to run rather than silently pick one; this covers two --namespace-dir sources colliding with each other just as much as one colliding with the repository's own namespaces/.  An override flag lifts this only for a prefix that collides with the repository's own namespaces/<prefix>/: the --namespace-dir version replaces it entirely, while every other, non-colliding prefix already in namespaces/ is still parsed and composed normally.  Two --namespace-dir sources colliding with each other has no override - there's no "repository's own" version for either to defer to, so that's always an error.

### Code Generation

Nothing in any generated library is ever hand-edited.  The repository has two kinds of directories: a set of per-language template directories holding hand-written, target-language-specific code (for example, a C++-only helper that has no Java or Python equivalent), and a separate, fully generated output directory per target language.  The generator reads the shared SED2 class/schema definitions plus the relevant template directory and writes the complete, self-contained library into the generated directory - one that can be dropped in and used as-is, without needing the templates directory alongside it.  Regenerating always overwrites the generated directories in full; any hand-written code that needs to survive regeneration lives only in the template directories.

### Math
SED2 element can have infix math as string children.  Create an ASTNode class, borrowing the rough interface from libsbml's ASTNode class, without the XML dependency, and inspired by its base bison 'l3' parser to convert infix strings, including the [] selectors, and expanded to include references-that-start-with-a-hash, a new colon syntax for subelements, and a dot syntax for non-structural subelements.

#### Lexer
The new lexer will have to distinguish text subelements (#a:b.c) from decimal numbers (1.3).  

#### Predefined Functions
In addition to the MathML functions and constants used in libsbml, new functions will need to be added, including:
* All the functions listed in the 'distrib' SBML package
* Any new function listed in the SED2 specification.

### Validation
The JSON schema is a fast, coarse first pass: it rejects structurally malformed documents (wrong types, missing required fields, pattern mismatches) with a human-readable message, but its errors are not numbered.  None of the three schema-validator libraries expose a reliable way to map a schema failure back to a stable rule number - pboettch in particular reports only the instance location and a free-text message, with no schema-location or constraint-keyword information (a pull request adding a keyword field is still open and unmerged, and its author declined to add schema-location tracking at all) - so numbering can't be built on top of the schema libraries' own error output.

Instead, every constraint that needs a stable, testable number - including ones a schema could also catch, like a required field or a pattern - is its own hand-written, numbered check in validate(), the same way libSBML doesn't rely on its XML parser's diagnostics for numbering either.  Numbers are appended to the end of the spec as they're discovered.  Each class should have a validate() function that calls its children recursively, so the parent 'document' class's 'validate' function validates the entire document.  All validation errors are collected and presented to the user as a list.

Overall, the model here is the SBML specification (C:\Users\Lucian\Desktop\sbml-specifications\sbml-level-3\version-2\core\spec\sbml-level-3-version-2-release-2-core.pdf) and the libsbml library (C:\Users\Lucian\Desktop\libsbml), though for JSON instead of XML.

#### Rule Documentation

Each numbered validation rule is documented as its own Markdown file in a validation/ subdirectory inside the rule's own class's Data Sheet folder - e.g. specsheets/tasks/ExplicitODESimulation/v1.0.0/validation/ExplicitODESimulation-0001.md, next to that class's schema.json and description.md. A rule lives with the class it constrains and versions with it, so a new version directory (see Versioning) gets its own validation/ directory rather than threading a change through a separate, centrally-numbered file.

Rule IDs are [ClassName]-NNNN (e.g. ExplicitODESimulation-0001), not a flat global number, since classes aren't drawn from one obviously-ordered list. IDs are append-only within a class's validation/ folder, same as the flat numbering scheme described above.  A namespace-owned class's rules follow a variant of this to stay collision-free and filename-safe - see Namespaces.

Each rule file is YAML frontmatter plus a prose body:

```
---
id: ExplicitODESimulation-0001
rule: The independentVariable of an ExplicitODESimulation must be a string.
message: "Reference '{value}' resolves to '{resolved-value}', which is not a string."
severity: error
status: active
---

Longer explanation, edge cases, examples - not surfaced in a validation
error, unlike rule/message above.
```

`rule` is the constraint stated plainly, for a rule catalog or docs. `message` is the template actually used to build a validation error's text, with placeholders filled in per offending instance:

| Placeholder | Meaning |
|---|---|
| `{class}` | class name of the element being validated |
| `{id}` | id of the element being validated |
| `{attr}` | the attribute that failed |
| `{value}` | the attribute's literal value as written - a plain literal, or the reference string itself if it's a reference |
| `{resolved-value}` | what `{value}` traces back to: itself for a literal, the target's literal value for a reference that resolves statically (e.g. to a constant); omitted when the reference can only be known at run time (e.g. a task's output) |
| `{expected-type}` | the type the rule requires |
| `{subvalue}` | the bracket/dot subelement portion of a reference, e.g. `['S1']` or `.model` |
| `{allowed}` | comma-separated list of allowed values, for enum-style rules |
| `{expr}` | a raw math/infix expression string, for AST well-formedness rules |
| `{min}` / `{max}` | numeric bounds, for range/cardinality rules |

#### Generated Rule Index

The generator emits one generated/rules-vX.json per distinct version string that appears as a directory name anywhere under specsheets/ (see Versioning) - e.g. if v1.0.0, v1.1.2, and v1.2.2 exist somewhere in the tree, it produces rules-v1.0.0.json, rules-v1.1.2.json, and rules-v1.2.2.json.  Each file aggregates every class's rules as resolved for that specific version - each class contributing from whichever of its own directories is newest without exceeding that version - giving a complete rules manifest for any version a document might declare.  It's generated fresh every run, not hand-maintained; the validation/ folders under specsheets/ stay the single source of truth.  Nothing at runtime reads it - each generated library's validate() checks compile their message templates directly into code - so it exists for tooling: a rule catalog, coverage checks, external docs.

### Cross-references

Almost every attribute in the document can have either a raw value ("5") or a reference to a value, as described in the spec.  These references will be stored as text strings in their attributes, and their classes will need the functions 'isReference' ('true' if the value is a string that starts with "#") and 'getSEDReference', which returns a non-owning pointer to the referenced element (or NULL if no such element exists).

The full description of how references work is in the spec, but briefly: document objects are referred to by a hashtag, then their parent/child relationship with colons:  "#tasks:task1:subtask2".  From there, subobjects might be referenced with dots (#tasks:task1.model)  If the object is a vector or a dictionary, subelements can use square brackets (#tasks:task1.model['S1'])  Thus, the validator needs to know if those subelement references are plausible, but will not be able to return a pointer to the particular sub-element: they are run-time values that will only become literal values when the experiment is actually being performed.  However, they can still be validated:  'hasSubvalue("string")' should return 'true' if (say) "[3]" or "['S1']" are legal subelements of the SED2 object.



## Prior work

A previous speculative python-based library, along with several tests and example documents, was developed at C:\Users\Lucian\Desktop\sed  Much of it is a translator, but the core class organization might be helpful, and the example JSON files should also be helpful, though it might contain used-to-be-valid documents, and shouldn't be taken as gospel a priori.