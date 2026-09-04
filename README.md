Implementation of a library to read and translate SED2 documents.

## Building and testing

```
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

CMake fetches its dependencies (nlohmann::json, pboettch/json-schema-validator, GoogleTest) automatically via `FetchContent` on first configure. Class boilerplate under `include/sed2/generated` and `src/generated` (per `codegen/spec_attributes/*.json`) is regenerated automatically by the build whenever a table or `codegen/generate_classes.py` changes.
