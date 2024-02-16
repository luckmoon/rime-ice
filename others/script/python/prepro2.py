#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import json
import os
from collections import defaultdict, Counter

import jieba
from common.io_utils import get_base_dir

BASE_CORPUS_DIR = get_base_dir()


def main():
    news2016zh_valid_file = os.path.join(BASE_CORPUS_DIR, "news2016zh_valid.json")
    news2016zh_train_file = os.path.join(BASE_CORPUS_DIR, "news2016zh_train.json")

    counter = Counter()
    for in_file in [news2016zh_valid_file, news2016zh_train_file]:
        with open(in_file, "r", encoding="utf-8") as fin:
            cnt = 0
            for line in fin:
                cnt += 1
                line = json.loads(line)
                content = line["content"]
                tokens = jieba.lcut(content)
                counter.update(tokens)
                if cnt > 100:
                    break
    print(counter.most_common())


if __name__ == '__main__':
    main()
