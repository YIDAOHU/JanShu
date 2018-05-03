# -*- coding: UTF-8 –*-

import re


def extract_num(text):
    # 从字符串中提取出数字
    match_re = re.match(".*?(\d+).*", text, re.S)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums
