## What is SED2?

SED stands for Simulation Experiment Description.  SED2 is a language for recording simulation experiments in JSON form that can be translated and exported to a number of different systems, where the core simulations and other analyses can be performed by a variety of tools.  It can be viewed as a generic workflow language, where instead of specific commands to a particular operating system and environment, it instead contains abstract commands that could be executed on a variety of operating systems and environments.

SED-ML was an earlier language (Simulation Experiment Description Markup Language), was XML-based, and tightly constrained.  The goal of SED2 is to change the format to JSON instead of XML, and expand the scope of what is possible to describe.

SED2 is designed to facilitate reproducibilty for the biological modeling community, much like SBML was desgned to facilitate model exchange for the biological modeling community.  In 20 years, the same SED2 document should be readable by a new library using new simulators and programs that don't exist today, and they should still produce the same results.

Ultimately, a SED2 'orchestrator' should be able to read a SED2 file, figure out who to ask to do each task, then stitch everything together to perform an efficient execution of all the tasks described in the document.

The SED2 specification document original is a Google Doc, and all of the UML diagrams are Google Draw documents.  A copy PDF is available as "SED2 2026.pdf" in the root directory.  It may be updated as the project goes on, and the user will need to update the Google Doc by hand if so.

## General Strategy

We want a C++ library that reads and validates SED2 files, and can be used to create or otherwise manipulate a SED2 file.  The SED2 design may change, and it definitely will expand with time, so it also needs to flexibly changeable.

In a future project, we will use this library to write a translator of SED2 to a python script, a Julia script, and a Process Bigraph JSON file.  This library is constrained to serve as the base for those future translators.

## Testing

Everything should be test-driven.  We need tests for valid and invalid SED2 documents, and for each function (i.e. get/set).  We will use google tests, the same way that libantimony does (C:\Users\Lucian\Desktop\antimony).

The github project should be set to run tests on pushes.

## Design

Use C++17 as the base.

### JSON Library

The library will use nlohmann::json (https://github.com/nlohmann/json) as the underlying JSON parser and DOM.  It is header-only, MIT-licensed, requires only C++11, and has strong MSVC support, so it is easy to bring into the build without a separate compiled dependency.  Its dynamic tree also lets each SED2 class keep any unrecognized fields around unchanged, which matters given the format is expected to expand over time.

For the JSON-schema pass mentioned under Validation below, we'll use pboettch/json-schema-validator (https://github.com/pboettch/json-schema-validator), since it validates directly against an nlohmann::json document rather than requiring a separate conversion step.

### Classes
Each SED2 class should have a corresponding C++ class.  The classes are defined by the '_type' child, Each child attribute is owned by its parent, and should have get-, set- isSet- and unset- functions.  Each class will have a predefined list of child attributes, defined in the specification.

Some child objects themselves are lists, for example, the 'tasks' child of the document.  'getTasks', then should return an ordered list of tasks, with each task being its own subclass type, defined by its "_type" attribute.  List children need a list API, as well: add- (append at end), remove- (remove the child with the given ID), and insert- (place in list at given index).

### Math
SED2 element can have infix math as string children.  Create an ASTNode class, borrowing the rough interface from libsbml's ASTNode class, without the XML dependency, and inspired by its base bison 'l3' parser to convert infix strings, including the [] selectors, and expanded to include references-that-start-with-a-hash, a new colon syntax for subelements, and a dot syntax for non-structural subelements.

#### Lexer
The new lexer will have to distinguish text subelements (#a:b.c) from decimal numbers (1.3).  

#### Predefined Functions
In addition to the MathML functions and constants used in libsbml, new functions will need to be added, including:
* All the functions listed in the 'distrib' SBML package
* Any new function listed in the SED2 specification.

### Validation
General validation can be performed by a JSON schema.  More specific validation errors that cannot be checked by a schema are generally described in the spec, but need to be numbered and appended to the end of the spec as they are discovered.  Each class should have a validate() function that calls its children recursively, so the parent 'document' class's 'validate' function validates the entire document.  All validation errors are collected and presented to the user as a list.

Overall, the model here is the SBML specification (C:\Users\Lucian\Desktop\sbml-specifications\sbml-level-3\version-2\core\spec\sbml-level-3-version-2-release-2-core.pdf) and the libsbml library (C:\Users\Lucian\Desktop\libsbml), though for JSON instead of XML.

### Cross-references

Almost every attribute in the document can have either a raw value ("5") or a reference to a value, as described in the spec.  These references will be stored as text strings in their attributes, and their classes will need the functions 'isReference' ('true' if the value is a string that starts with "#") and 'getSEDReference', which returns a non-owning pointer to the referenced element (or NULL if no such element exists).

The full description of how references work is in the spec, but briefly: document objects are referred to by a hashtag, then their parent/child relationship with colons:  "#tasks:task1:subtask2".  From there, subobjects might be referenced with dots (#tasks:task1.model)  If the object is a vector or a dictionary, subelements can use square brackets (#tasks:task1.model['S1'])  Thus, the validator needs to know if those subelement references are plausible, but will not be able to return a pointer to the particular sub-element: they are run-time values that will only become literal values when the experiment is actually being performed.  However, they can still be validated:  'hasSubvalue("string")' should return 'true' if (say) "[3]" or "['S1']" are legal subelements of the SED2 object.



## Prior work

A previous speculative python-based library, along with several tests and example documents, was developed at C:\Users\Lucian\Desktop\sed  Much of it is a translator, but the core class organization might be helpful, and the example JSON files should also be helpful, though it might contain used-to-be-valid documents, and shouldn't be taken as gospel a priori.