// processor.h

#ifndef PROCESSOR_H
#define PROCESSOR_H

#include "cppjieba/Jieba.hpp"
#include "cppjieba/limonp/StringUtil.hpp"
#include <future>
#include <string>
#include <unordered_map>
#include <utils.h>
#include <vector>
// #include "json/json.h"

class Processor {

public:
  Processor(cppjieba::Jieba *jieba);
  void run();

private:
  void _init_files();
  void _load_cn_tokens();
  TokenCounter process_one_by_jieba(std::string &file);
  TokenCounter process_one_by_jieba2(std::vector<std::string> &lines, long start, long end);
  TokenCounter process_wiki();
  TokenCounter process_one_by_split(std::string &file);
  TokenCounter process_weibo();
  TokenCounter process_douban();
  TokenCounter process_tieba();
  void dump_new_freq();

public:
  TokenCounter token_counter;
  std::vector<std::string> yaml_files;

private:
  std::string _base_dir;
  std::unordered_set<std::string> all_tokens;
  cppjieba::Jieba *_jieba;
};

#endif // PROCESSOR_H
