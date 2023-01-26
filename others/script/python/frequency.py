from functools import partial, reduce
import glob
import json
import os

import yaml
import jieba
from pyhanlp import HanLP
from tqdm import tqdm
from collections import Counter
import getpass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# warm up
jieba.lcut("1234")

USERNAME = getpass.getuser()
# tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
HanLP.Config.ShowTermNature = False
yaml_files = glob.glob("../../../cn_dicts/*.yaml")
# yaml_files = ["../../../cn_dicts/ext.dict.yaml"]


def load_all_token():
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
    in_files = glob.glob(f"/Users/{USERNAME}/Downloads/raw_chat_corpus/weibo-400w/*")
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
    in_files = glob.glob(f"/Users/{USERNAME}/Downloads/raw_chat_corpus/douban-multiturn-100w/*")
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
    in_files = glob.glob(f"/Users/{USERNAME}/Downloads/raw_chat_corpus/tieba-305w/*")
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
    in_files = glob.glob(f"/Users/{USERNAME}/Downloads/wiki_zh/*/*")
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


def dump_new_freq(counter):
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
                        dump_line = line + "\n"

                if line == "...":
                    flag = True
                fout.write(dump_line)
        fout.close()


def main():
    token_set = load_all_token()
    counter = Counter()
    process_wiki(counter, token_set)
    print(counter.most_common(100))
    dump_new_freq(counter)


def main2():
    token_set = load_all_token()
    counter = Counter()

    in_files = glob.glob(f"/Users/{USERNAME}/Downloads/wiki_zh/*/*")
    with ProcessPoolExecutor(max_workers=4) as executor:
        with tqdm(total=len(in_files)) as progress:
            futures = []
            for in_file in in_files:
                future = executor.submit(
                    process_single_wiki, in_file, token_set)
                future.add_done_callback(lambda p: progress.update())
                futures.append(future)
            result = [x.result() for x in futures]
    counter = reduce(lambda x, y: x+y, result)

    weibo_counter = process_weibo(token_set)
    counter = counter + weibo_counter

    douban_counter = process_douban(token_set)
    counter = counter + douban_counter

    tieba_counter = process_tieba(token_set)
    counter = counter + tieba_counter

    print(counter.most_common(100))
    dump_new_freq(counter)


if __name__ == "__main__":
    # main()
    main2()
