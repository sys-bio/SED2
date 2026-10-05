// Release smoke test for the C++ source package: parse and validate one SED2
// document through the packaged library. Exit status 0 means the document
// parsed and produced no validation problems. See CMakeLists.txt here.
#include <iostream>

#include <libsed2/DirectOnly.hpp>
#include <libsed2/Io.hpp>

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: smoke <document.sed2.json>\n";
        return 2;
    }
    auto doc = libsed2::read_from_file(argv[1]);
    auto problems = doc->validate();
    for (const auto& p : problems) std::cerr << "problem: " << p.rule_id << "\n";
    std::cout << argv[1] << ": " << problems.size() << " validation problem(s)\n";
    return problems.empty() ? 0 : 1;
}
