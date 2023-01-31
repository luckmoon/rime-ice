import datetime


def get_dict_header(name):
    dt = datetime.datetime.now().strftime("%Y-%m-%d")

    header = f"""
---
name: {name}
version: "{dt}"
sort: by_weight
...
    """

    return header
