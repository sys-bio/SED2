// Generated half of the JavaScript API (see templates/js/src/api.cpp for the
// fixed half): the entry points whose values come from the spec or from
// VERSION.txt. GENERATED - do not hand-edit; regenerate via
// generator/generate.py.
#include <emscripten.h>

extern "C" {

/// Library version (VERSION.txt at generate time).
EMSCRIPTEN_KEEPALIVE const char* sed2_library_version() { return "0.1.0"; }

/// Newest SED2 document-format version this library knows.
EMSCRIPTEN_KEEPALIVE const char* sed2_document_version() { return "v1.0.0"; }

/// JSON array of every generated class name.
EMSCRIPTEN_KEEPALIVE const char* sed2_class_names() { return "[\"AggregationCalculation\",\"Annotation\",\"Axis\",\"BoundedODESimulation\",\"BoundedStochasticSimulation\",\"Calculation\",\"CreateDataBlock\",\"CsvImport\",\"Curve\",\"DataImport\",\"DrawFromDistribution\",\"ExplicitODESimulation\",\"ExplicitStochasticSimulation\",\"FluxBalanceAnalysis\",\"JacobianFull\",\"JacobianReduced\",\"Loop\",\"LoopVariable\",\"ModelChange\",\"ModelElementList\",\"ModelImport\",\"NumericRange\",\"OneStepODESimulation\",\"OneStepStochasticSimulation\",\"OutputParameter\",\"ParameterRange\",\"ParameterScan\",\"Plot2D\",\"Plot3D\",\"Range\",\"RelabelData\",\"Report\",\"SEDDocument\",\"Scatter\",\"Span\",\"SteadyState\",\"StringFormation\",\"Style\",\"Surface\",\"TaskParameter\",\"WorkingAlgorithm\"]"; }

}  // extern "C"
