#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pypinyin
import jieba


def cut_3(txt):
    cut_list = list(jieba.lcut(txt, cut_all = True))
    length = len(cut_list)

    # 1，三个字是字是连一起的，无法拆分
    if length == 1:
        return "2", "2", "3"

    # 2，三个字可以拆分成：情况一： (3, 2)，情况二：(2, 3)， 情况三：(2, 1)， 情况四：(1， 2)， 情况五：(2, 2)
    if length == 2:
        # 情况一：(3, 2)
        if len(cut_list[0]) == 3 and len(cut_list[1]) == 2:
            return "3", "2", "3"

        # 情况二：(2, 3)
        if len(cut_list[0]) == 2 and len(cut_list[1]) == 3:
            return "2", "2", "3"

        # 情况三：(2, 1)
        if len(cut_list[0]) == 2 and len(cut_list[1]) == 1:
            return "2", "2", "3"

        # 情况四：(1, 2)
        if len(cut_list[0]) == 1 and len(cut_list[1]) == 2:
            return "3", "2", "3"

        # 情况五：(2, 2)
        if len(cut_list[0]) == 3 and len(cut_list[1]) == 2:
            return "2", "2", "3"

    # 3，三个字可以拆分成：情况一：(2, 3, 2)，情况二：(1，1，1)
    if length == 3:
        # 情况一：(2, 3, 2)
        if len(cut_list[0]) == 1 and len(cut_list[1]) == 1 and len(cut_list[2]) == 1:
            return "2", "2", "3"

        # 情况二：(1, 1, 1)
        if len(cut_list[0]) == 1 and len(cut_list[1]) == 1 and len(cut_list[2]) == 1:
            return "2", "2", "3"


def correct_tone3(txt: str, pys: list):
    # 找出三个连续的
    for i in range(2, len(pys)):
        if pys[i][-1] == '3' and pys[i - 1][-1] == '3' and pys[i - 2][-1] == '3':
            # 根据分词判断变调
            first, sec, _ = cut_3(txt[i - 2: i + 1])
            pys[i - 2] = pys[i - 2][:-1] + first
            pys[i - 1] = pys[i - 1][:-1] + sec

    # 找出只有两个连续的
    for i in range(1, len(pys)):
        if pys[i][-1] == '3' and pys[i - 1][-1] == '3':
            pys[i - 1] = pys[i - 1][:-1] + '2'

    return pys


gp_number = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "零"]


def correct_yi_bu(txt: str, pys: list):
    # 一在末尾念第一声
    if txt[-1] == "一":
        pys[-1] = "yi1"

    for i in range(len(pys) - 1):
        if txt[i] == "不":
            # 在第四声字前念第二声，否则念第四声
            if pys[i + 1][-1] == '4':
                pys[i] = 'bu2'
            else:
                pys[i] = 'bu4'
        elif txt[i] == "一":
            # 在第四声字前念第二声，否则念第四声
            if pys[i + 1][-1] == '4':
                pys[i] = 'yi2'
            else:
                pys[i] = 'yi4'

    # “一”“不”夹在动词当中念轻声。
    for i in range(2, len(pys)):
        if txt[i - 2] == txt[i]:
            if txt[i - 1] == "不":
                pys[i - 1] = "bu5"
            elif txt[i - 1] == "一":
                pys[i - 1] = "yi5"

    for i in range(len(pys) - 1):
        # 如果是数字，念第一声
        if txt[i] == "一" and txt[i + 1] in gp_number:
            pys[i] = 'yi1'

    return pys


def _correct_tone5(pys):
    for i in range(len(pys)):
        if pys[i][-1] not in '1234':
            pys[i] += '5'
    return pys


SPECIAL_NOTES = '。？！?!.;；:,，: ""\"\"\'\''


def gp2py(text: str):
    pys = pypinyin.pinyin(text, pypinyin.TONE3, neutral_tone_with_five=True)
    pys = [p[0] for p in pys]
    correct_tone3(text, pys)
    correct_yi_bu(text, pys)
    return pys
