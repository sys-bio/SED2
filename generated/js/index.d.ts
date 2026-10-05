// TypeScript declarations for the JavaScript build. GENERATED - do not
// hand-edit; regenerate via generator/generate.py.

/** Name of a generated SED2 class. */
export type ClassName = "AggregationCalculation" | "Annotation" | "Axis" | "BoundedODESimulation" | "BoundedStochasticSimulation" | "Calculation" | "CreateDataBlock" | "CsvImport" | "Curve" | "DataImport" | "DrawFromDistribution" | "ExplicitODESimulation" | "ExplicitStochasticSimulation" | "FluxBalanceAnalysis" | "JacobianFull" | "JacobianReduced" | "Loop" | "LoopVariable" | "ModelChange" | "ModelElementList" | "ModelImport" | "NumericRange" | "OneStepODESimulation" | "OneStepStochasticSimulation" | "OutputParameter" | "ParameterRange" | "ParameterScan" | "Plot2D" | "Plot3D" | "Range" | "RelabelData" | "Report" | "SEDDocument" | "Scatter" | "Span" | "SteadyState" | "StringFormation" | "Style" | "Surface" | "TaskParameter" | "WorkingAlgorithm";

export interface Problem {
  ruleId: string;
  severity: string;
  rule: string;
  message: string;
  location: string;
}

/** ok:false means the input could not be processed at all (e.g. malformed JSON). */
export type ValidateResult = { ok: true; problems: Problem[] } | { ok: false; error: string };

export interface Sed2 {
  /** Version of this library. */
  version(): string;
  /** Newest SED2 document-format version this library knows (e.g. "v1.0.0"). */
  documentVersion(): string;
  classNames(): ClassName[];
  /** Keys accepted by validateObject(). */
  directOnlyKeys(): string[];
  ruleCatalog(): Record<string, { rule: string; message: string; severity: string }>;
  /** Parse and validate a SED2 document. */
  validate(text: string): ValidateResult;
  /** Validate one direct-only class instance, selected by a key from directOnlyKeys(). */
  validateObject(key: string, text: string): ValidateResult;
  /** Parse a document and write it back out in canonical form. */
  normalize(text: string): { ok: true; text: string } | { ok: false; error: string };
  /** Syntax-check a SED2 math string. */
  checkMath(text: string): { ok: true } | { ok: false; error: string };
}

/** Wraps an instantiated Emscripten module. */
export function wrap(module: unknown): Sed2;
/** Loads the module (Node) and wraps it; modulePath defaults to the sibling build output. */
export function load(modulePath?: string): Promise<Sed2>;
