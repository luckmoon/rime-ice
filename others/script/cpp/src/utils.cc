#include "utils.h"
#include "cppjieba/limonp/StringUtil.hpp"
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <pwd.h>
#include <set>
#include <string>
#include <sys/types.h>
#include <unistd.h>
#include <vector>

namespace utils {
std::vector<std::string> findFiles(const std::string &directory) {
  std::cout << "process directory: " << directory << std::endl;

  std::vector<std::string> files;
  for (const auto &entry :
       ghc::filesystem::recursive_directory_iterator(directory)) {
    // if (entry.is_regular_file() && entry.path().extension() == ".txt") {
    if (entry.is_regular_file()) {
      files.push_back(entry.path().string());
    }
  }

  int num = std::min((int)files.size(), 100000);
  std::vector<std::string>::const_iterator first = files.begin();
  std::vector<std::string>::const_iterator last = files.begin() + num;
  std::vector<std::string> newVec(first, last);
  return newVec;
}

std::vector<std::string> findFiles(const std::string &directory,
                                   const std::string &suffix) {
  std::vector<std::string> files;

  for (const auto &entry :
       ghc::filesystem::recursive_directory_iterator(directory)) {
    if (entry.is_regular_file() && entry.path().extension() == suffix) {
      files.push_back(entry.path().string());
    }
  }

  return files;
}

std::vector<std::string> findDirectories(const std::string &directory) {
  std::vector<std::string> dirs;
  for (const auto &entry : ghc::filesystem::directory_iterator(directory)) {
    if (ghc::filesystem::is_directory(entry)) {
      dirs.emplace_back(entry.path().string());
    }
  }
  return dirs;
}

std::string get_home_path() {
  struct passwd *pw = getpwuid(getuid());
  const char *homedir = pw->pw_dir;
  return std::string(homedir);
}

void update_counter(std::vector<std::string> &words,
                    std::unordered_set<std::string> &filter_set,
                    TokenCounter &counter) {
  for (auto &token : words) {
    if (filter_set.find(token) == filter_set.end())
      continue;

    auto it = counter.find(token);
    if (it != counter.end()) {
      counter[token] = counter[token] + 1;
    } else {
      counter[token] = 1;
    }
  }
}

TokenCounter merge_counter(std::vector<TokenCounter> &counters) {
  TokenCounter ret;
  for (auto &counter : counters) {
    for (const auto &pair : counter) {
      auto it = ret.find(pair.first);
      if (it != ret.end()) {
        it->second += pair.second;
      } else {
        ret.insert(pair);
      }
    }
  }
  return ret;
}

void merge_counter(TokenCounter &ret, TokenCounter &counter) {
  for (const auto &pair : counter) {
    auto it = ret.find(pair.first);
    if (it != ret.end()) {
      it->second += pair.second;
    } else {
      ret.insert(pair);
    }
  }
}

bool sortByValue(const std::pair<std::string, long> &a,
                 const std::pair<std::string, long> &b) {
  return a.second > b.second; // 按值降序排序
}

void printTopK(TokenCounter &counter, int topK) {
  // 将 map 中的键值对拷贝到 vector 中
  std::vector<std::pair<std::string, long>> vec(counter.begin(), counter.end());

  std::sort(vec.begin(), vec.end(), sortByValue);

  std::cout << "Top K values:\n";
  int count = 0;
  for (const auto &pair : vec) {
    std::cout << pair.first << ": " << pair.second << "\t\t";
    count++;
    if (count == topK) {
      break;
    }
  }
  std::cout << "\n";
}

} // namespace utils
