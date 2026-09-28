// Hand-written glue: runs every test-specsheets/fixtures/*.sed2.json
// fixture through the generated libsed2test library's parser + validate(),
// and checks it against the rule ID(s)/count(s) encoded in the filename -
// see Design.md's Testing section for the naming convention this parses.
//
// This file lives under templates/cpp/tests/ (hand-written, never
// regenerated - see Design.md's Code Generation section) and is copied
// alongside the generated library, under tests/, for the CMake-built
// `fixture_tests` GoogleTest binary to run. It is the C++ analog of
// templates/python/tests/test_fixtures.py - see that file for the
// reference implementation this one mirrors, including its fix for the
// chain-suffix parsing bug (a rule ID's own trailing NNNN segment is
// always 4 digits, never a chain-count boundary).

#include <sed2test/Io.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <dirent.h>
#include <fstream>
#include <functional>
#include <map>
#include <memory>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace sed2test;

namespace {

std::string fixtures_dir() {
    const char* env = std::getenv("SED2_FIXTURES_DIR");
    if (env && *env) return std::string(env);
    return "../../../../fixtures";
}

std::vector<std::string> fixture_files() {
    std::vector<std::string> files;
    DIR* dir = opendir(fixtures_dir().c_str());
    if (!dir) return files;
    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        std::string name(entry->d_name);
        if (name.size() > 10 && name.substr(name.size() - 10) == ".sed2.json") {
            files.push_back(fixtures_dir() + "/" + name);
        }
    }
    closedir(dir);
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

const std::map<std::string, std::function<std::unique_ptr<SedBase>()>>& direct_classes() {
    static const std::map<std::string, std::function<std::unique_ptr<SedBase>()>> m = {
        {"Choice-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<Choice>()); }},
        {"WeightedChoice-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<WeightedChoice>()); }},
        {"SimpleWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<SimpleWidget>()); }},
        {"FancyWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<FancyWidget>()); }},
        {"SimpleReport-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<SimpleReport>()); }},
        {"acme-AcmeWidget-0002", [] { return std::unique_ptr<SedBase>(std::make_unique<AcmeWidget>()); }},
    };
    return m;
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

    std::vector<ValidationProblem> problems;
    std::string direct_key;
    for (const auto& kv : direct_classes()) {
        if (base.rfind(kv.first, 0) == 0) {
            direct_key = kv.first;
            break;
        }
    }

    if (!direct_key.empty()) {
        std::unique_ptr<SedBase> obj = direct_classes().at(direct_key)();
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
