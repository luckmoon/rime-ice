#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import json
import os
import datetime

from abc import ABCMeta, abstractmethod
import re

import hanlp
import jieba
from common.io_utils import get_base_dir, get_tokenized_dir

import toml


BASE_CORPUS_DIR = get_base_dir()
DUMP_CORPUS_DIR = get_tokenized_dir()
if not os.path.isdir(DUMP_CORPUS_DIR):
    os.makedirs(DUMP_CORPUS_DIR)


class BaseTokenizer(metaclass=ABCMeta):
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
        print(f"{self.__class__.__name__} warmed up")


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
        print(f"{self.__class__.__name__} warmed up")


class WordSpaceTokinzer(BaseTokenizer):
    def __init__(self) -> None:
        super().__init__()
        pass

    def cut_line(self, line: str) -> list[str]:
        return line.split()

    def cut_lines(self, lines: list[str]) -> list[list[str]]:
        return [line.split() for line in lines]


class TokenizerFactory:
    @staticmethod
    def get_tokenizer(name: str) -> BaseTokenizer:
        if name == "jieba":
            return JiebaTokenzier()
        elif name == "hanlp":
            return HanlpTokenizer()
        elif name == "space":
            return WordSpaceTokinzer()
        else:
            raise ValueError(f"[{name}] tokenizer is not supported!")


TOKENIZER_MAP = {
    k: TokenizerFactory.get_tokenizer(k) for k in ["jieba", "hanlp", "space"]
}


class BaseLineParser(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def parse(self, line):
        pass


class JsonLineParser(BaseLineParser):
    def __init__(self, key: str) -> None:
        self.key = key

    def parse(self, line):
        line = json.loads(line)
        line = line[self.key]
        return line


class VanillaLineParser:
    def __init__(self) -> None:
        pass

    def parse(line):
        return line.strip()


class LineParserFactory:
    @staticmethod
    def get_parser(parser_name, **kwargs):
        if parser_name == "json":
            key = kwargs["key"]
            assert key is not None
            return JsonLineParser(key=key)
        elif parser_name == "vanilla":
            return VanillaLineParser()
        else:
            raise ValueError(f"[{parser_name}] parser is not supported!")


def save_to_file(tokens: list[list[str]], fout):
    for line in tokens:
        line = " ".join(line)
        fout.write(line + "\n")


def cut_one_file(
    in_abs_file: str,
    fout,
    tokenizer: BaseTokenizer,
    parser: BaseLineParser,
    batch_size: int,
) -> None:
    print(f"in_abs_file: {in_abs_file}")
    with open(in_abs_file, "r", encoding="utf-8") as fin:
        cnt = 0
        batch = []
        for line in fin:
            content = parser.parse(line)
            for sent in re.split("[。，；！？：.,;!?:]", content):
                if sent.strip() != "":
                    if len(sent) > 1000:
                        sents = sent.split()
                        for sent in sents:
                            if len(sent) > 1000:
                                print(sent)
                                continue
                            batch.append(sent)
                            cnt += 1
                    else:
                        batch.append(sent)
                        cnt += 1

            if cnt >= batch_size:
                tokens = tokenizer.cut_lines(batch)
                save_to_file(tokens, fout)
                cnt = 0
                batch = []


def main():
    config_file = "./config.toml"
    with open(config_file, "r") as fin:
        config = toml.load(fin)
    print(config)

    # {'news2016': {'tokenizer': 'hanlp', 'batch_size': 5, 'source_mode': 'direcotry', 'pattern': 'news2016zh_*.json'}}
    for _, value in config.items():
        print(value)

        tokenzier_name = value["tokenizer"]
        tokenzier = TOKENIZER_MAP[tokenzier_name]

        batch_size = value["batch_size"]

        dump_file = value["dump_file"]
        out_abs_file = os.path.join(DUMP_CORPUS_DIR, dump_file)

        pattern = value["pattern"]
        pattern = os.path.join(BASE_CORPUS_DIR, pattern)
        print(pattern)

        parser_name = value["parser"]
        key = value.get("key", None)
        parser = LineParserFactory.get_parser(parser_name, key=key)

        news2016zh_files = glob.glob(pattern)
        print(news2016zh_files)

        start_datetime = datetime.datetime.now()
        with open(out_abs_file, "w") as fout:
            for in_abs_file in news2016zh_files:
                cut_one_file(in_abs_file, fout, tokenzier, parser, batch_size)

        end_datetime = datetime.datetime.now()
        print(end_datetime - start_datetime)


if __name__ == "__main__":
    main()
