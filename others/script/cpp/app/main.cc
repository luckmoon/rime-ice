#include "cppjieba/Jieba.hpp"
#include "ghc/filesystem.hpp"
#include "processor.h"
#include <iostream>

namespace tokenizer {
std::string dict_path = ghc::filesystem::absolute("../data/jieba.dict.utf8");
std::string model_path = ghc::filesystem::absolute("../data/hmm_model.utf8");
std::string user_dict_path = ghc::filesystem::absolute("../data/user.dict.utf8");
std::string idf_path = ghc::filesystem::absolute("../data/idf.utf8");
std::string stop_word_path =
    ghc::filesystem::absolute("../data/stop_words.utf8");
} // namespace tokenizer

int main() {
  std::cout << "hello" << std::endl;

  // _init_jieba();
  cppjieba::Jieba _jieba(tokenizer::dict_path, tokenizer::model_path,
                         tokenizer::user_dict_path, tokenizer::idf_path,
                         tokenizer::stop_word_path);
  cppjieba::Jieba *jieba = &_jieba;

  std::vector<std::string> words;
  jieba->Cut("我是谁", words, true);

  Processor processor(jieba);
  processor.run();

  return 0;
}