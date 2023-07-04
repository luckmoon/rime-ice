#ifndef UTILS_H
#define UTILS_H

#include "ghc/filesystem.hpp"
#include <future>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using TokenCounter = std::unordered_map<std::string, long>;

namespace utils {
// trim from start (in place)
static inline void ltrim(std::string &s) {
  s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
            return !std::isspace(ch);
          }));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
  s.erase(std::find_if(s.rbegin(), s.rend(),
                       [](unsigned char ch) { return !std::isspace(ch); })
              .base(),
          s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
  rtrim(s);
  ltrim(s);
}

static inline void replaceAll(std::string& str, const std::string& from, const std::string& to) {
    if(from.empty())
        return;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // In case 'to' contains 'from', like replacing 'x' with 'yx'
    }
}

std::vector<std::string> findFiles(const std::string &directory);
std::vector<std::string> findFiles(const std::string &directory,
                                   const std::string &suffix);
std::vector<std::string> findDirectories(const std::string &directory);

std::string get_home_path();

void update_counter(std::vector<std::string> &words,
                    std::unordered_set<std::string> &filter_set,
                    TokenCounter &counter);
TokenCounter merge_counter(std::vector<TokenCounter> &counters);
void merge_counter(TokenCounter &ret, TokenCounter &counter);

void printTopK(TokenCounter &counter, int topK);

} // namespace utils
#endif // UTILS_H
