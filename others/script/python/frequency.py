import getpass
import glob
import json
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from enum import Enum
from functools import reduce

import jieba
# from pyhanlp import HanLP
from tqdm import tqdm

# warm up
jieba.lcut("1234")


class Platform(Enum):
    windows = 1
    mac = 2
    linux = 3
    others = 4


def get_platform():
    import platform
    sys_platform = platform.platform().lower()
    if "windows" in sys_platform:
        return Platform.windows
    elif "macos" in sys_platform:
        return Platform.mac
    elif "linux" in sys_platform:
        return Platform.linux
    else:
        return Platform.others


def get_base_dir():
    platform = get_platform()
    username = getpass.getuser()

    if platform == Platform.mac:
        return f"/Users/{username}/Downloads/rime_corpus"
    elif platform == Platform.linux:
        return f"/home/{username}/Downloads/rime_corpus"
    else:
        raise ValueError()


def load_cn_tokens():
    """
    加载cn_dicts下的词表
    :return:
    """
    all_tokens = set()
    for yaml_file in yaml_files:
        flag = False
        with open(yaml_file, "r") as fin:
            for line in fin:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                if line == "...":
                    flag = True
                    continue
                if flag:
                    line = line.split("\t")
                    if len(line) == 3:
                        token, pinyin, freq = line
                    elif len(line) == 2:
                        token, freq = line
                    elif len(line) == 1:
                        token, = line
                    else:
                        print("WARNING:", line)
                    all_tokens.add(token)
    # for idx, token in enumerate(all_tokens):
    #     if idx > 100:
    #         break
    #     print(token)
    print("len(all_tokens):", len(all_tokens))
    return all_tokens


def process_single_wiki(in_file, token_set):
    """
    统计wiki_zh中的词频
    :param in_file:
    :param token_set:
    :return:
    """
    counter = Counter()
    with open(in_file, "r") as fin:
        for line in fin.readlines():
            line = json.loads(line)
            text = line["text"]
            tokens = jieba.lcut(text)
            # tokens = tok(text)
            # tokens = HanLP.segment(text)
            # tokens = [x.word for x in tokens]
            tokens = [x for x in tokens if x in token_set]
            counter.update(tokens)
    return counter


def process_weibo(token_set):
    counter = Counter()
    in_files = glob.glob(f"{BASE_CORPUS_DIR}/raw_chat_corpus/weibo-400w/*")
    for in_file in in_files:
        print(in_file)
        with open(in_file, "r") as fin:
            for line in fin:
                line = line.strip()
                tokens = line.split()
                tokens = [token for token in tokens if token in token_set]
                counter.update(tokens)
    return counter


def process_douban(token_set):
    counter = Counter()
    in_files = glob.glob(f"{BASE_CORPUS_DIR}/raw_chat_corpus/douban-multiturn-100w/*")
    for in_file in in_files:
        print(in_file)
        with open(in_file, "r") as fin:
            for line in fin:
                line = line.strip()
                tokens = line.split()
                tokens = [token for token in tokens if token in token_set]
                counter.update(tokens)
    return counter


def process_tieba(token_set):
    counter = Counter()
    in_files = glob.glob(f"{BASE_CORPUS_DIR}/raw_chat_corpus/tieba-305w/*")
    for in_file in in_files:
        print(in_file)
        with open(in_file, "r") as fin:
            for line in fin:
                line = line.strip()
                tokens = jieba.lcut(line)
                tokens = [token for token in tokens if token in token_set]
                counter.update(tokens)
    return counter


def process_wiki(counter, token_set):
    """
    dropped
    :param counter:
    :param token_set:
    :return:
    """
    in_files = glob.glob(f"{BASE_CORPUS_DIR}/wiki_zh/*/*")
    for in_file in tqdm(in_files):
        with open(in_file, "r") as fin:
            for line in fin.readlines():
                line = json.loads(line)
                text = line["text"]
                tokens = jieba.lcut(text)
                # tokens = HanLP.segment(text)
                # tokens = [x.word for x in tokens]
                tokens = [x for x in tokens if x in token_set]
                counter.update(tokens)


def process_wiki_parallel(token_set):
    in_files = glob.glob(f"{BASE_CORPUS_DIR}/wiki_zh/*/*")
    with ProcessPoolExecutor(max_workers=4) as executor:
        with tqdm(total=len(in_files)) as progress:
            futures = []
            for in_file in in_files:
                future = executor.submit(
                    process_single_wiki, in_file, token_set)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)
            result = [x.result() for x in futures]
    counter = reduce(lambda x, y: x + y, result)
    return counter


def dump_new_freq(counter):
    """
    将基于自己的语料统计的词频保存到cn_dicts_freq中
    :param counter:
    :return:
    """
    for yaml_file in yaml_files:
        filename = os.path.basename(yaml_file)
        out_file = f"../../../cn_dicts_freq/{filename}"
        print(out_file)
        fout = open(out_file, "w")
        flag = False
        with open(yaml_file, "r") as fin:
            for line in fin:
                line = line.strip()
                dump_line = line + "\n"
                if flag:
                    line = line.split("\t")
                    if len(line) == 3:
                        token, pinyin, freq = line
                        freq = counter.get(token, 1)
                        dump_line = f"{token}\t{pinyin}\t{freq}\n"
                    elif len(line) == 2:
                        token, freq = line
                        freq = counter.get(token, 1)
                        dump_line = f"{token}\t{freq}\n"
                    elif len(line) == 1:
                        token, = line
                        dump_line = f"{token}\n"
                    else:
                        print("WARNING:", line)
                        dump_line = f"{line}\n"

                if line == "...":
                    flag = True
                fout.write(dump_line)
        fout.close()


def main():
    token_set = load_cn_tokens()
    counter = Counter()
    process_wiki(counter, token_set)
    print(counter.most_common(100))
    dump_new_freq(counter)


def main2():
    token_set = load_cn_tokens()
    counter = Counter()

    wiki_counter = process_wiki_parallel(token_set)
    counter = counter + wiki_counter

    weibo_counter = process_weibo(token_set)
    counter = counter + weibo_counter

    douban_counter = process_douban(token_set)
    counter = counter + douban_counter

    tieba_counter = process_tieba(token_set)
    counter = counter + tieba_counter

    print(counter.most_common(100))
    dump_new_freq(counter)


if __name__ == "__main__":
    # tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
    # HanLP.Config.ShowTermNature = False
    # yaml_files = ["../../../cn_dicts/ext.dict.yaml"]
    yaml_files = glob.glob("../../../cn_dicts/*.yaml")
    BASE_CORPUS_DIR = get_base_dir()
    print(BASE_CORPUS_DIR)

    # main()
    main2()
