#include "cppjieba/Jieba.hpp"
#include "ghc/filesystem.hpp"
#include "processor.h"
#include <iostream>

namespace tokenizer {
std::string dict_path = ghc::filesystem::absolute("../data/jieba.dict.utf8");
std::string model_path = ghc::filesystem::absolute("../data/hmm_model.utf8");
std::string user_dict_path =
    ghc::filesystem::absolute("../data/user.dict.utf8");
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

  // std::string file = "/tmp/temp3.txt";
  // 三叫鼠，又名三吱儿、蜜唧
  // 在HMM=true下，和python版jieba对不上
  // HMM=false下，有其他case
  // 总之和python版对不上
  std::string file = "/tmp/temp5.txt";

  std::string line;
  std::cout << file << std::endl;
  std::ifstream infile(file.c_str());
  if (infile.is_open()) {
    std::cout << "=====" << std::endl;
    while (std::getline(infile, line)) {
      std::istringstream iss(line);
      std::vector<std::string> words;
      jieba->Cut(line, words, true);
      std::cout << words.size() << std::endl;

      // for (auto &x : words) {
      //   std::cout << x << std::endl;
      // }
    }

    infile.close();
  }

  return 0;
}