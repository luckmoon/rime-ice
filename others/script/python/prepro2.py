#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import datetime

from abc import ABC, abstractmethod
from typing import Union

import hanlp
import jieba
from common.io_utils import get_base_dir

BASE_CORPUS_DIR = get_base_dir()


class BaseTokenizer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def cut_line(self, line: str) -> list[str]:
        pass

    @abstractmethod
    def cut_lines(self, lines: list[str]) -> list[list[str]]:
        pass


class JiebaTokenzier(BaseTokenizer):
    def __init__(self) -> None:
        super().__init__()
        self._warmup()

    def cut_line(self, line: str) -> list[str]:
        return jieba.lcut(line)

    def cut_lines(self, lines: list[str]) -> list[list[str]]:
        return [jieba.lcut(line) for line in lines]

    def _warmup(self):
        self.cut_line("南京市长江大桥")


class HanlpTokenizer(BaseTokenizer):
    def __init__(self) -> None:
        super().__init__()
        self.tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
        self._warmup()

    def cut_line(self, line: str) -> list[str]:
        return self.tok(line)

    def cut_lines(self, lines: list[str]) -> list[list[str]]:
        return self.tok(lines)

    def _warmup(self):
        self.cut_line("南京市长江大桥")


class TokenizerFactory:
    @staticmethod
    def get_tokenizer(name: str = "jieba"):
        if name == "jieba":
            return JiebaTokenzier()
        elif name == "hanlp":
            return HanlpTokenizer()
        else:
            raise ValueError(f"[{name}] tokenizer is not supported!")


def cut_line(tokenizer: BaseTokenizer, line: Union[str, list[str]]):
    tokens = tokenizer.cut_line(line)
    return tokens


def main():
    # tokenizer_name = "jieba"
    tokenizer_name = "hanlp"
    tokenzier = TokenizerFactory.get_tokenizer(tokenizer_name)
    batch_size = 5

    news2016zh_valid_file = os.path.join(BASE_CORPUS_DIR, "news2016zh_valid.json")
    news2016zh_train_file = os.path.join(BASE_CORPUS_DIR, "news2016zh_train.json")

    start_datetime = datetime.datetime.now()
    for in_file in [news2016zh_valid_file, news2016zh_train_file]:
        with open(in_file, "r", encoding="utf-8") as fin:
            cnt = 0
            batch = []
            for line in fin:
                if cnt >= batch_size:
                    tokens = tokenzier.cut_lines(batch)
                    print(tokens)
                    cnt = 0
                    batch = []

                    break

                cnt += 1
                line = json.loads(line)
                content = line["content"]
                batch.append(content)

    end_datetime = datetime.datetime.now()
    print(end_datetime - start_datetime)


if __name__ == "__main__":
    main()
