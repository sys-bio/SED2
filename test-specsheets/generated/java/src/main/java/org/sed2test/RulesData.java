package org.sed2test;

/** Generated rule catalogue. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class RulesData {
    private RulesData() {}

    public static void register() {
        RuleCatalog.CATALOG.put("AbstractReport-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to AbstractReport that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("AbstractReport-0001", new RuleCatalog.Entry("The format attribute of an AbstractReport, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"));
        RuleCatalog.CATALOG.put("AbstractReport-0002", new RuleCatalog.Entry("A value that must resolve to a concrete AbstractReport subtype must declare a _type attribute.", "{location} must be an AbstractReport, but no _type at all was declared.", "error"));
        RuleCatalog.CATALOG.put("AbstractWidget-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to AbstractWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("AbstractWidget-0001", new RuleCatalog.Entry("The label attribute of an AbstractWidget, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"));
        RuleCatalog.CATALOG.put("AbstractWidget-0002", new RuleCatalog.Entry("A value that must resolve to a concrete AbstractWidget subtype must declare a _type attribute.", "{location} must be an AbstractWidget, but no _type at all was declared.", "error"));
        RuleCatalog.CATALOG.put("Choice-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to Choice that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("Choice-0002", new RuleCatalog.Entry("The _type attribute of a Choice must be \"choice\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
        RuleCatalog.CATALOG.put("Choice-0003", new RuleCatalog.Entry("The label attribute of a Choice, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"));
        RuleCatalog.CATALOG.put("FancyWidget-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to FancyWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("FancyWidget-0001", new RuleCatalog.Entry("The value attribute of a FancyWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("FancyWidget-0002", new RuleCatalog.Entry("The _type attribute of a FancyWidget must be \"fancyWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
        RuleCatalog.CATALOG.put("Note-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to Note that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("Note-0001", new RuleCatalog.Entry("The text attribute of a Note is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("SimpleReport-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to SimpleReport that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("SimpleReport-0001", new RuleCatalog.Entry("The source attribute of a SimpleReport is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("SimpleReport-0002", new RuleCatalog.Entry("The _type attribute of a SimpleReport must be \"simpleReport\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
        RuleCatalog.CATALOG.put("SimpleWidget-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to SimpleWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("SimpleWidget-0001", new RuleCatalog.Entry("The value attribute of a SimpleWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("SimpleWidget-0002", new RuleCatalog.Entry("The _type attribute of a SimpleWidget must be \"simpleWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
        RuleCatalog.CATALOG.put("SimpleWidget-acme-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to the acme namespace's own additions to SimpleWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("SimpleWidget-acme-0001", new RuleCatalog.Entry("If present, the acme@priority attribute of a SimpleWidget must be non-negative.", "Attribute '{attr}' of {class} '{id}' must be >= 0.", "error"));
        RuleCatalog.CATALOG.put("TestBase-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to TestBase that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("TestBase-0001", new RuleCatalog.Entry("The name attribute of a TestBase-derived element, if present, must be a string.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string.", "error"));
        RuleCatalog.CATALOG.put("TestDocument-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to TestDocument that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("TestDocument-0001", new RuleCatalog.Entry("The version attribute of a TestDocument is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("TestDocument-0002", new RuleCatalog.Entry("The widgets attribute of a TestDocument, if present, must be an object whose values are AbstractWidget objects.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractWidget objects.", "error"));
        RuleCatalog.CATALOG.put("TestDocument-0003", new RuleCatalog.Entry("The reports attribute of a TestDocument, if present, must be an object whose values are AbstractReport objects.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an object whose values are AbstractReport objects.", "error"));
        RuleCatalog.CATALOG.put("WeightedChoice-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to WeightedChoice that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("WeightedChoice-0001", new RuleCatalog.Entry("The weight attribute of a WeightedChoice is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("WeightedChoice-0002", new RuleCatalog.Entry("The _type attribute of a WeightedChoice must be \"weightedChoice\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
        RuleCatalog.CATALOG.put("WidgetOptions-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to WidgetOptions that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("WidgetOptions-0001", new RuleCatalog.Entry("The retries attribute of a WidgetOptions-composing class, if present, must be a non-negative integer.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a non-negative integer.", "error"));
        RuleCatalog.CATALOG.put("WidgetOptions-0002", new RuleCatalog.Entry("The timeoutSeconds attribute of a WidgetOptions-composing class, if present, must be a positive number.", "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive number.", "error"));
        RuleCatalog.CATALOG.put("acme-AcmeWidget-0000", new RuleCatalog.Entry("The element fails a JSON Schema constraint attributable to acme@AcmeWidget that does not match any other numbered rule.", "{schema-message} (at {location})", "error"));
        RuleCatalog.CATALOG.put("acme-AcmeWidget-0001", new RuleCatalog.Entry("The acme@acmeLevel attribute of an acme@AcmeWidget is required.", "Required attribute '{attr}' is missing from {class} '{id}'.", "error"));
        RuleCatalog.CATALOG.put("acme-AcmeWidget-0002", new RuleCatalog.Entry("The _type attribute of an acme@AcmeWidget must be \"acme@acmeWidget\".", "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'.", "error"));
    }
}
