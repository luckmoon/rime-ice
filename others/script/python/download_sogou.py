#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}
name = "网络流行新词【官方推荐】"
URL = f"https://download.pinyin.sogou.com/dict/download_cell.php?id=4&name={name}"


def main():
    resp = requests.get(URL, timeout=5, headers=HEADERS)
    print(resp.status_code)
    os.makedirs("/tmp/scel", exist_ok=True)
    path = f"/tmp/scel/{name}.scel"
    with open(path, "wb") as fw:
        fw.write(resp.content)


if __name__ == '__main__':
    main()
