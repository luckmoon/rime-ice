"""
百度个人词库处理
Mac v5.4.0.10 可以导出txt版本的
"""

import getpass
from common.header import get_dict_header

USERNAME = getpass.getuser()

in_file = f"/Users/{USERNAME}/Downloads/百度mac词库导出2023_01_31"
name = "baidu_personal"
out_file = f"../../../ext_dicts/{name}.dict.yaml"


with open(in_file, "r", encoding="utf-16") as fin, open(out_file, "w") as fout:
    header = get_dict_header(name)
    fout.write(header + "\n")

    for line in fin:
        # 草稿纸(cao|gao|zhi) 60001
        line = line.strip()
        token_pinyin, freq = line.split(" ")
        token_pinyin = token_pinyin.replace("(", " ").replace(")", " ")
        token, pinyin = token_pinyin.split()
        pinyin = pinyin.replace("|", " ")
        print(token, pinyin, freq)
        line = f"{token}\t{pinyin}\t{freq}"
        fout.write(line + "\n")
