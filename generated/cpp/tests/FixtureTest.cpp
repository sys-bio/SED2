// Hand-written glue: runs every fixture in this tree's fixtures/ directory
// through the generated library's parser + validate(), and checks it
// against the rule ID(s)/count(s) encoded in the filename - see Design.md's
// Testing section for the naming convention this parses.
//
// This file lives under templates/cpp/tests/ (hand-written, never
// regenerated - see Design.md's Code Generation section) and is copied,
// with its #include/using-namespace lines rewritten to match --cpp-
// namespace, to <out>/cpp/tests/FixtureTest.cpp as part of every
// `generate.py` run that includes the cpp target (see
// generator/emit_cpp.py's _copy_fixture_test_cpp) - never by hand, so a
// fresh spec regeneration always carries a matching, up-to-date copy with
// it. It is the C++ analog of templates/python/tests/test_fixtures.py -
// see that file for the reference implementation this one mirrors,
// including its fix for the chain-suffix parsing bug (a rule ID's own
// trailing NNNN segment is always 4 digits, never a chain-count boundary).
//
// Nothing below is specific to any one spec tree (test-specsheets/ vs.
// specsheets/, or any future one): read_from_string()/write_to_string()
// already operate on whatever the document root type is without this file
// naming it (auto doc = read_from_string(...)), and which classes need
// "direct" (not document-embedded) validation is resolved through
// direct_only_classes() - a table built by the generator itself at
// generate time (see emit_cpp.py's emit_direct_only_hpp), since C++ has no
// runtime reflection to discover it the way Python and Java do. The
// #include path and using-namespace line are the one exception - the
// preprocessor needs a literal namespace name - so the generator rewrites
// only those at copy time.

#include <libsed2/DirectOnly.hpp>
#include <libsed2/Io.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace libsed2;

namespace {

namespace fs = std::filesystem;

/// CMakeLists.txt (see _cmake_lists in generator/emit_cpp.py) bakes in
/// SED2_FIXTURES_DIR_DEFAULT as this module's own known path to fixtures/
/// (CMAKE_CURRENT_SOURCE_DIR/../../fixtures - always correct, independent
/// of --cpp-namespace and of whatever working directory the test binary
/// ends up run from) - the C++ equivalent of the Java target's generated
/// pom.xml sed2.fixturesDir system property. SED2_FIXTURES_DIR remains the
/// highest-priority override for CI/manual runs, same as the other two
/// targets; the plain relative fallback below only matters if this file is
/// ever compiled outside that generated CMakeLists.txt.
std::string fixtures_dir() {
    const char* env = std::getenv("SED2_FIXTURES_DIR");
    if (env && *env) return std::string(env);
#ifdef SED2_FIXTURES_DIR_DEFAULT
    return SED2_FIXTURES_DIR_DEFAULT;
#else
    return "../../fixtures";
#endif
}

/// True if `file` (somewhere under `base`) has "archive" as one of its
/// directory components relative to base - deprecated-rule fixtures,
/// excluded from the active suite (see Design.md's Repository Layout
/// section).
bool under_archive_dir(const fs::path& base, const fs::path& file) {
    fs::path rel = fs::relative(file.parent_path(), base);
    for (const auto& part : rel) {
        if (part == "archive") return true;
    }
    return false;
}

/// Every *.sed2.json anywhere under fixtures_dir(), except beneath an
/// "archive" subdirectory. Recursive so this picks up fixtures/generated/,
/// fixtures/handwritten/, and any future subdirectory Design.md's layout
/// adds, without this file needing to know about any of them by name.
std::vector<std::string> fixture_files() {
    std::vector<std::string> files;
    fs::path base = fixtures_dir();
    std::error_code ec;
    if (!fs::is_directory(base, ec)) return files;
    for (const auto& entry : fs::recursive_directory_iterator(base, ec)) {
        if (!entry.is_regular_file()) continue;
        const fs::path& p = entry.path();
        std::string name = p.filename().string();
        if (name.size() > 10 && name.substr(name.size() - 10) == ".sed2.json" && !under_archive_dir(base, p)) {
            files.push_back(p.string());
        }
    }
    std::sort(files.begin(), files.end());
    return files;
}

std::string basename_of(const std::string& path) {
    auto pos = path.find_last_of('/');
    return pos == std::string::npos ? path : path.substr(pos + 1);
}

std::string read_file(const std::string& path) {
    std::ifstream f(path);
    std::stringstream ss;
    ss << f.rdbuf();
    return ss.str();
}

struct Expected {
    std::string kind;
    std::vector<std::pair<std::string, int>> rules;
};

const std::regex& fixture_re() {
    static const std::regex re(
        R"(^([A-Za-z0-9_-]+)-(pass|fail)-(\d+)-(.+?)((?:-[A-Za-z0-9_-]+-\d+)*)\.sed2\.json$)");
    return re;
}

Expected expected_from_filename(const std::string& base) {
    if (base.rfind("pass-", 0) == 0) {
        return Expected{"pass", {}};
    }
    std::smatch m;
    bool matched = std::regex_match(base, m, fixture_re());
    EXPECT_TRUE(matched) << "fixture name doesn't match convention: " << base;
    std::string rule = m[1].str();
    std::string kind = m[2].str();
    int count = std::stoi(m[3].str());
    std::string chain = m[5].str();

    Expected expected;
    expected.kind = kind;
    expected.rules.push_back({rule, count});

    if (!chain.empty()) {
        std::string stripped = chain;
        while (!stripped.empty() && stripped.front() == '-') stripped.erase(stripped.begin());
        std::vector<std::string> parts;
        std::stringstream ss(stripped);
        std::string tok;
        while (std::getline(ss, tok, '-')) parts.push_back(tok);

        // A chain segment is "<rule-id-tokens...>-<count>". Rule ids
        // themselves always end in a 4-digit NNNN segment, while a chain
        // count uses the same short (1-2 digit) width used elsewhere in
        // the filename - so only a non-4-digit numeric token ends a
        // segment (see test_fixtures.py's fix, mirrored here).
        std::vector<size_t> nums;
        for (size_t i = 0; i < parts.size(); i++) {
            bool all_digit = !parts[i].empty() &&
                    std::all_of(parts[i].begin(), parts[i].end(), [](unsigned char c) { return std::isdigit(c); });
            if (all_digit && parts[i].size() != 4) nums.push_back(i);
        }
        size_t start = 0;
        for (size_t idx : nums) {
            std::string rid;
            for (size_t j = start; j < idx; j++) {
                if (!rid.empty()) rid += "-";
                rid += parts[j];
            }
            int cnt = std::stoi(parts[idx]);
            expected.rules.push_back({rid, cnt});
            start = idx + 1;
        }
    }
    return expected;
}

}  // namespace

class FixtureTest : public ::testing::TestWithParam<std::string> {};

TEST_P(FixtureTest, RunsFixture) {
    std::string path = GetParam();
    std::string base = basename_of(path);
    Expected expected = expected_from_filename(base);
    std::string raw_text = read_file(path);
    jsoncons::json instance = jsoncons::json::parse(raw_text);

    register_rules();

    std::string primary_rule = expected.rules.empty() ? "" : expected.rules[0].first;
    const auto& direct = direct_only_classes();
    auto direct_it = direct.find(primary_rule);

    std::vector<ValidationProblem> problems;
    if (direct_it != direct.end()) {
        std::unique_ptr<SedBase> obj = direct_it->second();
        load_fields(obj.get(), instance);
        problems = obj->validate();
    } else {
        auto doc = read_from_string(raw_text);
        problems = doc->validate();
        if (expected.kind == "pass") {
            jsoncons::json rt = jsoncons::json::parse(write_to_string(*doc));
            EXPECT_EQ(rt, instance) << "round-trip mismatch for " << path;
        }
    }

    if (expected.kind == "pass") {
        EXPECT_TRUE(problems.empty()) << path << " expected to pass, got " << problems.size() << " problem(s)";
        return;
    }

    std::map<std::string, int> counts;
    for (const auto& p : problems) counts[p.rule_id]++;

    for (const auto& e : expected.rules) {
        int got = counts.count(e.first) ? counts[e.first] : 0;
        EXPECT_EQ(got, e.second) << path << ": expected rule " << e.first << " to fire " << e.second
                                  << " time(s), got " << got;
    }
    std::set<std::string> allowed;
    for (const auto& e : expected.rules) allowed.insert(e.first);
    for (const auto& kv : counts) {
        EXPECT_TRUE(allowed.count(kv.first)) << path << ": unexpected extra violation " << kv.first
                                              << " fired " << kv.second << " time(s)";
    }
}

INSTANTIATE_TEST_SUITE_P(AllFixtures, FixtureTest, ::testing::ValuesIn(fixture_files()),
                         [](const ::testing::TestParamInfo<std::string>& info) {
                             std::string name = basename_of(info.param);
                             std::string sanitized;
                             for (char c : name) sanitized += (std::isalnum(static_cast<unsigned char>(c)) ? c : '_');
                             return sanitized;
                         });
