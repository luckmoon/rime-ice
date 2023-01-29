#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO
先将语料进行切词，然后保存下来，便于重复利用
"""

import getpass
import glob
import json
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import reduce

import time
import jieba
import json
from pyhanlp import HanLP
import hanlp

from tqdm import tqdm

USERNAME = getpass.getuser()

# warm up
jieba.lcut("1234")
# tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
tok = hanlp.load(hanlp.pretrained.tok.MSR_TOK_ELECTRA_BASE_CRF)
HanLP.Config.ShowTermNature = False

BASE_CORPUS_DIR = f"/Users/{USERNAME}/Downloads/rime_corpus"
BASE_OUT_DIR = f"/Users/{USERNAME}/Downloads/rime_corpus_tokenized"

if not os.path.isdir(BASE_OUT_DIR):
    os.makedirs(BASE_OUT_DIR)


def tokenize_jieba(text):
    return " ".join(jieba.lcut(text))


def tokenize_hanlp_v1(text):
    tokens = HanLP.segment(text)
    tokens = [token.word for token in tokens]
    return " ".join(tokens)


def tokenize_hanlp_v2(text):
    tokens = tok(text)
    return " ".join(tokens)


def tokenize_hanlp_v2_batch(batch_texts):
    tokens = tok(batch_texts)
    return [" ".join(x) for x in tokens]


def main():
    in_files = ["/Users/tiantianzheng/Downloads/rime_corpus/wiki_zh/AF/wiki_37"]
    for in_file in in_files:
        filename = os.path.basename(in_file)
        out_file = os.path.join(BASE_OUT_DIR, filename)
        with open(in_file, "r") as fin, open(out_file, "w") as fout:
            for line in fin.readlines():
                line = json.loads(line)
                text = line["text"]
                ret_jieba = tokenize_jieba(text)
                ret_hanlp_v1 = tokenize_hanlp_v1(text)
                ret_hanlp_v2 = tokenize_hanlp_v2(text)
                ret = {"jieba": ret_jieba,
                       "hanlp_v1": ret_hanlp_v1,
                       "hanlp_v2": ret_hanlp_v2}
                fout.write(json.dumps(ret, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    texts = ["我爱北京天安门", "白日依山尽", "小狼毫输入法什么时候要是有智能纠错功能的话就好了"]
    for sent in texts:
        print(tokenize_jieba(sent))
        print(tokenize_hanlp_v1(sent))
        print(tokenize_hanlp_v1(sent))
    print(tokenize_hanlp_v2_batch(texts))

    main()
