// Generated rule catalogue for libsed2test. GENERATED - do not hand-edit;
// regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

namespace sed2test {

inline void register_rules() {
    static bool done = false;
    if (done) return;
    done = true;
    RuleCatalog::catalog()["AbstractReport-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to AbstractReport that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["AbstractReport-0001"] = RuleCatalog::Entry{"The format attribute of an AbstractReport, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"};
    RuleCatalog::catalog()["AbstractReport-0002"] = RuleCatalog::Entry{"A value that must resolve to a concrete AbstractReport subtype must declare a _type attribute.", "{location} must be an AbstractReport, but no _type at all was declared.", "error"};
    RuleCatalog::catalog()["AbstractWidget-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to AbstractWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["AbstractWidget-0001"] = RuleCatalog::Entry{"The label attribute of an AbstractWidget, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"};
    RuleCatalog::catalog()["AbstractWidget-0002"] = RuleCatalog::Entry{"A value that must resolve to a concrete AbstractWidget subtype must declare a _type attribute.", "{location} must be an AbstractWidget, but no _type at all was declared.", "error"};
    RuleCatalog::catalog()["Choice-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to Choice that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["Choice-0002"] = RuleCatalog::Entry{"The _type attribute of a Choice must be \"choice\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
    RuleCatalog::catalog()["Choice-0003"] = RuleCatalog::Entry{"The label attribute of a Choice, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"};
    RuleCatalog::catalog()["FancyWidget-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to FancyWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["FancyWidget-0001"] = RuleCatalog::Entry{"The value attribute of a FancyWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["FancyWidget-0002"] = RuleCatalog::Entry{"The _type attribute of a FancyWidget must be \"fancyWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
    RuleCatalog::catalog()["Note-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to Note that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["Note-0001"] = RuleCatalog::Entry{"The text attribute of a Note is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["SimpleReport-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to SimpleReport that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["SimpleReport-0001"] = RuleCatalog::Entry{"The source attribute of a SimpleReport is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["SimpleReport-0002"] = RuleCatalog::Entry{"The _type attribute of a SimpleReport must be \"simpleReport\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
    RuleCatalog::catalog()["SimpleWidget-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to SimpleWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["SimpleWidget-0001"] = RuleCatalog::Entry{"The value attribute of a SimpleWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["SimpleWidget-0002"] = RuleCatalog::Entry{"The _type attribute of a SimpleWidget must be \"simpleWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
    RuleCatalog::catalog()["SimpleWidget-acme-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to the acme namespace's own additions to SimpleWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["SimpleWidget-acme-0001"] = RuleCatalog::Entry{"If present, the acme@priority attribute of a SimpleWidget must be non-negative.", "Attribute '{attr}' of {class} '{id}' must be >= 0.", "error"};
    RuleCatalog::catalog()["TestBase-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to TestBase that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["TestBase-0001"] = RuleCatalog::Entry{"The name attribute of a TestBase-derived element, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"};
    RuleCatalog::catalog()["TestDocument-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to TestDocument that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["TestDocument-0001"] = RuleCatalog::Entry{"The version attribute of a TestDocument is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["TestDocument-0002"] = RuleCatalog::Entry{"The widgets attribute of a TestDocument, if present, must be an object whose values are AbstractWidget objects.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractWidget objects.", "error"};
    RuleCatalog::catalog()["TestDocument-0003"] = RuleCatalog::Entry{"The reports attribute of a TestDocument, if present, must be an object whose values are AbstractReport objects.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractReport objects.", "error"};
    RuleCatalog::catalog()["WeightedChoice-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to WeightedChoice that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["WeightedChoice-0001"] = RuleCatalog::Entry{"The weight attribute of a WeightedChoice is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["WeightedChoice-0002"] = RuleCatalog::Entry{"The _type attribute of a WeightedChoice must be \"weightedChoice\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
    RuleCatalog::catalog()["WidgetOptions-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to WidgetOptions that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["WidgetOptions-0001"] = RuleCatalog::Entry{"The retries attribute of a WidgetOptions-composing class, if present, must be a non-negative integer.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a non-negative integer.", "error"};
    RuleCatalog::catalog()["WidgetOptions-0002"] = RuleCatalog::Entry{"The timeoutSeconds attribute of a WidgetOptions-composing class, if present, must be a positive number.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive number.", "error"};
    RuleCatalog::catalog()["acme-AcmeWidget-0000"] = RuleCatalog::Entry{"The element fails a JSON Schema constraint attributable to acme@AcmeWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"};
    RuleCatalog::catalog()["acme-AcmeWidget-0001"] = RuleCatalog::Entry{"The acme@acmeLevel attribute of an acme@AcmeWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"};
    RuleCatalog::catalog()["acme-AcmeWidget-0002"] = RuleCatalog::Entry{"The _type attribute of an acme@AcmeWidget must be \"acme@acmeWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"};
}

}  // namespace sed2test
