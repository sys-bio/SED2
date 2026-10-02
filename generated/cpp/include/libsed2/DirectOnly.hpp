// Generated direct-only-class registry (see this file's own generator,
// generator/emit_cpp.py's emit_direct_only_hpp, for what this is and why
// it exists). GENERATED - do not hand-edit; regenerate via
// generator/generate.py.
#pragma once

#include "GeneratedModel.hpp"

#include <functional>
#include <map>
#include <memory>
#include <string>

namespace libsed2 {

inline const std::map<std::string, std::function<std::unique_ptr<SedBase>()>>& direct_only_classes() {
    static const std::map<std::string, std::function<std::unique_ptr<SedBase>()>> m = {
        {"AggregationCalculation-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<AggregationCalculation>()); }},
        {"BoundedODESimulation-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<BoundedODESimulation>()); }},
        {"BoundedStochasticSimulation-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<BoundedStochasticSimulation>()); }},
        {"Calculation-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<Calculation>()); }},
        {"CreateDataBlock-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<CreateDataBlock>()); }},
        {"CsvImport-0018", [] { return std::unique_ptr<SedBase>(std::make_unique<CsvImport>()); }},
        {"DataImport-0007", [] { return std::unique_ptr<SedBase>(std::make_unique<DataImport>()); }},
        {"DrawFromDistribution-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<DrawFromDistribution>()); }},
        {"ExplicitODESimulation-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<ExplicitODESimulation>()); }},
        {"ExplicitStochasticSimulation-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<ExplicitStochasticSimulation>()); }},
        {"FluxBalanceAnalysis-0008", [] { return std::unique_ptr<SedBase>(std::make_unique<FluxBalanceAnalysis>()); }},
        {"JacobianFull-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<JacobianFull>()); }},
        {"JacobianReduced-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<JacobianReduced>()); }},
        {"Loop-0005", [] { return std::unique_ptr<SedBase>(std::make_unique<Loop>()); }},
        {"ModelChange-0011", [] { return std::unique_ptr<SedBase>(std::make_unique<ModelChange>()); }},
        {"ModelElementList-0011", [] { return std::unique_ptr<SedBase>(std::make_unique<ModelElementList>()); }},
        {"ModelImport-0007", [] { return std::unique_ptr<SedBase>(std::make_unique<ModelImport>()); }},
        {"NumericRange-0013", [] { return std::unique_ptr<SedBase>(std::make_unique<NumericRange>()); }},
        {"OneStepODESimulation-0007", [] { return std::unique_ptr<SedBase>(std::make_unique<OneStepODESimulation>()); }},
        {"OneStepStochasticSimulation-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<OneStepStochasticSimulation>()); }},
        {"ParameterRange-0016", [] { return std::unique_ptr<SedBase>(std::make_unique<ParameterRange>()); }},
        {"ParameterScan-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<ParameterScan>()); }},
        {"Range-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<Range>()); }},
        {"RelabelData-0006", [] { return std::unique_ptr<SedBase>(std::make_unique<RelabelData>()); }},
        {"Scatter-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<Scatter>()); }},
        {"SteadyState-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<SteadyState>()); }},
        {"StringFormation-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<StringFormation>()); }},
        {"Plot2D-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<Plot2D>()); }},
        {"Plot3D-0004", [] { return std::unique_ptr<SedBase>(std::make_unique<Plot3D>()); }},
        {"Report-0003", [] { return std::unique_ptr<SedBase>(std::make_unique<Report>()); }},
        {"Curve-0012", [] { return std::unique_ptr<SedBase>(std::make_unique<Curve>()); }},
        {"Span-0007", [] { return std::unique_ptr<SedBase>(std::make_unique<Span>()); }},
    };
    return m;
}

}  // namespace libsed2
