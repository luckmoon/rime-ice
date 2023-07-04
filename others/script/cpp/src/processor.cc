#include "processor.h"
#include "cppjieba/Jieba.hpp"
#include "processor.h"
#include "utils.h"
#include <alloca.h>
#include <cstddef>
#include <fstream>
#include <functional>
#include <iostream>
#include <new>
#include <nlohmann/json.hpp>
#include <ostream>
#include <sched.h>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utils.h>
#include <vector>

Processor::Processor(cppjieba::Jieba *jieba) : _jieba(jieba) {
  std::cout << "Processor constructor" << std::endl;
  std::string home_dir = utils::get_home_path();
  _base_dir = home_dir + "/Downloads/rime_corpus";
  std::cout << _base_dir << std::endl;

  _init_files();
  _load_cn_tokens();
}

void Processor::_init_files(void) {
  yaml_files = utils::findFiles("../../../../cn_dicts", ".yaml");
  std::cout << "found yaml_files number: " << yaml_files.size() << std::endl;
}

void Processor::_load_cn_tokens() {

  for (auto &yaml_file : yaml_files) {
    bool flag = false;

    std::string line;
    std::cout << yaml_file << std::endl;
    std::ifstream infile(yaml_file.c_str());
    while (std::getline(infile, line)) {
      std::istringstream iss(line);
      utils::trim(line);
      if (line == "" or limonp::StartsWith(line, "#")) {
        continue;
      }
      if (line == "...") {
        flag = true;
        continue;
      }
      if (flag) {
        std::vector<std::string> tmp;
        limonp::Split(line, tmp, "\t");

        std::string token;
        std::string pinyin;
        // std::string freq;
        if (tmp.size() == 3) {
          token = tmp[0];
          pinyin = tmp[1];
          // freq = tmp[2];
        } else if (tmp.size() == 2) {
          token = tmp[0];
          // freq = tmp[1];
        } else if (tmp.size() == 1) {
          token = tmp[0];
        } else {
          std::cout << "WARNING: _load_cn_tokens: " << line << std::endl;
        }

        all_tokens.insert(token);
      }
    }
    infile.close();
  }

  std::cout << "all_tokens.size: " << all_tokens.size() << std::endl;
}

TokenCounter Processor::process_one_by_jieba(std::string &dir) {
  TokenCounter counter;

  std::vector<std::string> files = utils::findFiles(dir);

  for (auto &file : files) {
    std::string line;
    std::ifstream infile(file.c_str());
    while (std::getline(infile, line)) {
      std::istringstream iss(line);

      // Json::Value root;
      // Json::Reader reader;
      // reader.parse(line, root);
      // line = root["text"].asString();

      nlohmann::json root = nlohmann::json::parse(line);
      line = root["text"];

      utils::replaceAll(line, "\n", " ");

      std::vector<std::string> words;
      _jieba->Cut(line, words, true);
      utils::update_counter(words, all_tokens, counter);
    }
    infile.close();
  }

  return counter;
}

TokenCounter Processor::process_one_by_jieba2(std::vector<std::string> &lines,
                                              long start, long end) {
  TokenCounter counter;
  std::cout << "start:" << start << ", end:" << end << std::endl;
  for (size_t i = start; i < end; i++) {
    if (i >= lines.size()) {
      break;
    }
    std::vector<std::string> words;
    _jieba->Cut(lines[i], words, true);
    utils::update_counter(words, all_tokens, counter);
  }

  return counter;
}

TokenCounter Processor::process_wiki() {
  std::vector<TokenCounter> counters;

  std::vector<std::string> dirs;
  for (auto &x : utils::findDirectories(_base_dir + "/wiki_zh")) {
    dirs.emplace_back(x);
  }
  std::cout << "found dirs number: " << dirs.size() << std::endl;

  std::vector<std::future<TokenCounter>> futures;

  // for (auto &file : files) {
  //   TokenCounter counter = process_one_by_jieba(file);
  //   counters.push_back(counter);
  // }
  for (const auto &dir : dirs) {
    auto future =
        std::async(std::launch::async,
                   std::bind(&Processor::process_one_by_jieba, this, dir));
    futures.emplace_back(std::move(future));
  }
  for (auto &future : futures) {
    TokenCounter counter = future.get();
    counters.push_back(counter);
  }

  auto ret = utils::merge_counter(counters);

  std::cout << "ok wiki: " << ret.size() << std::endl;
  return ret;
}

TokenCounter Processor::process_one_by_split(std::string &file) {
  TokenCounter counter;
  std::cout << file << std::endl;
  std::string line;
  std::ifstream infile(file.c_str());
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    std::vector<std::string> words;
    limonp::Split(line, words, " \t\r\n");
    utils::update_counter(words, all_tokens, counter);
  }
  infile.close();
  return counter;
}

TokenCounter Processor::process_weibo() {
  std::cout << "start process weibo..." << std::endl;
  std::vector<std::string> files =
      utils::findFiles(_base_dir + "/raw_chat_corpus/weibo-400w");
  std::cout << "found files number: " << files.size() << std::endl;

  std::vector<std::future<TokenCounter>> futures;
  futures.reserve(files.size());

  for (auto &file : files) {
    auto future =
        std::async(std::launch::async,
                   std::bind(&Processor::process_one_by_split, this, file));
    futures.emplace_back(std::move(future));
  }

  std::vector<TokenCounter> counters;
  for (auto &future : futures) {
    TokenCounter counter = future.get();
    counters.push_back(counter);
  }

  auto ret = utils::merge_counter(counters);

  std::cout << "ok weibo: " << ret.size() << std::endl;
  return ret;
}

TokenCounter Processor::process_douban() {
  std::vector<std::string> files =
      utils::findFiles(_base_dir + "/raw_chat_corpus/douban-multiturn-100w");
  std::cout << "found files number: " << files.size() << std::endl;

  TokenCounter ret;
  for (auto &file : files) {
    TokenCounter counter = process_one_by_split(file);
    utils::merge_counter(ret, counter);
  }

  std::cout << "ok douban: " << ret.size() << std::endl;
  return ret;
}

TokenCounter Processor::process_tieba() {
  std::vector<std::string> files =
      utils::findFiles(_base_dir + "/raw_chat_corpus/tieba-305w");
  std::cout << "found files number: " << files.size() << std::endl;

  std::vector<std::string> lines;
  for (auto &file : files) {
    std::cout << file << std::endl;
    std::string line;
    std::ifstream infile(file.c_str());
    while (std::getline(infile, line)) {
      std::istringstream iss(line);
      lines.emplace_back(line);
    }
  }
  std::cout << "lines size: " << lines.size() << std::endl;

  int nGroups = 6;
  long groupSize = lines.size() / nGroups + 1;

  std::vector<std::future<TokenCounter>> futures;
  futures.reserve(nGroups);

  for (int i = 0; i < lines.size(); i += groupSize) {
    auto future = std::async(std::launch::async,
                             std::bind(&Processor::process_one_by_jieba2, this,
                                       lines, i, i + groupSize));
    futures.emplace_back(std::move(future));
  }

  std::vector<TokenCounter> counters;
  for (auto &future : futures) {
    TokenCounter counter = future.get();
    counters.push_back(counter);
  }

  auto ret = utils::merge_counter(counters);

  std::cout << "ok tieba: " << ret.size() << std::endl;
  return ret;
}

void Processor::dump_new_freq() {
  for (auto &yaml_file : yaml_files) {
    std::string filename = ghc::filesystem::path(yaml_file).filename();
    std::cout << "filename:" << filename << std::endl;
    std::string out_file = "../../../../cn_dicts_freq/" + filename;
    // std::string out_file = "/tmp/" + filename;
    bool flag = false;

    std::ofstream outstream(out_file);

    std::string line;
    std::cout << yaml_file << std::endl;
    std::ifstream instream(yaml_file.c_str());
    while (std::getline(instream, line)) {
      std::istringstream iss(line);
      utils::trim(line);
      std::string dump_line = line + "\n";
      if (flag) {
        std::vector<std::string> tmp;
        limonp::Split(line, tmp, "\t");
        std::string token;
        std::string pinyin;
        long freq;
        if (tmp.size() == 3) {
          token = tmp[0];
          pinyin = tmp[1];
          // freq = tmp[2];
          auto it = token_counter.find(token);
          freq = (it != token_counter.end() ? it->second : 1);
          dump_line =
              token + "\t" + pinyin + "\t" + std::to_string(freq) + "\n";
        } else if (tmp.size() == 2) {
          token = tmp[0];
          // freq = tmp[1];
          auto it = token_counter.find(token);
          freq = (it != token_counter.end() ? it->second : 1);
          dump_line = token + "\t" + std::to_string(freq) + "\n";
        } else if (tmp.size() == 1) {
          token = tmp[0];
          dump_line = token + "\n";
        } else {
          std::cout << "WARNING: dump_new_freq: " << line << std::endl;
          dump_line = line + "\n";
        }
      }

      if (line == "...") {
        flag = true;
      }

      outstream << dump_line;
    }

    instream.clear();
    outstream.close();
  }
}

void Processor::run() {
  TokenCounter counter;

  counter = process_wiki();
  utils::merge_counter(token_counter, counter);

  counter = process_weibo();
  utils::merge_counter(token_counter, counter);

  counter = process_douban();
  utils::merge_counter(token_counter, counter);

  counter = process_tieba();
  utils::merge_counter(token_counter, counter);

  utils::printTopK(token_counter, 100);

  dump_new_freq();
}
