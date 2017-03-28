#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import re
import MeCab

try:
    # python 2.x
    from itertools import izip
    zip = izip
except ImportError:
    pass

try:
    unicode # python 2.x
    def encodeMeCab(text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        return text
    def decodeMeCab(text):
        return text.decode('utf-8')
except:
    # With python 3.x, SWIG converts str into char* automatically.
    # so we do not convert them.
    def encodeMeCab(text):
        return text
    def decodeMeCab(text):
        return text

class GrongishTranslator(object):
    "グロンギ語-日本語の相互翻訳機"

    re_ltu = re.compile(u'ッ(.[ャュョァィゥェォ]?)')
    re_long = re.compile(u'(.[ャュョァィゥェォ]?)ー')
    _ja_dic = u'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモワダヂヅデドバビブベボパピプペポラリルレロ'
    _gr_dic = u'ガギグゲゴバビブベボガギグゲゴダヂヅデドバビブベボザジズゼゾラリルレロパザジズゼゾダヂヅデドマミムメモサシスセソ'
    _numbers = u'0123456789０１２３４５６７８９〇一二三四五六七八九零壱弐参'
    _gr_numbers = (
        u'ゼゼソ',
        u'パパン',
        u'ドググ',
        u'グシギ',
        u'ズゴゴ',
        u'ズガギ',
        u'ギブグ',
        u'ゲズン',
        u'ゲギド',
        u'バギン',
    )

    def __init__(self, fromdic=None, todic=None):
        self._totagger = None
        if todic:
            self._totagger = MeCab.Tagger('-d%s -r%s/dicrc -Oyomi' % (todic, todic))
        self._fromtagger = None
        if fromdic:
            self._fromtagger = MeCab.Tagger('-d%s -r%s/dicrc -Oyomi' % (fromdic, fromdic))

        self._num_dic = dict([(ch, i%10) for i, ch in enumerate(self._numbers)])
        self._num_dic[u'十'] = 10
        self._num_dic[u'百'] = 100
        self._num_dic[u'千'] = 1000
        self._num_dic[u'万'] = 10000
        self._num_dic[u'億'] = 100000000
        self._num_dic[u'兆'] = 1000000000000
        self._num_dic[u'京'] = 10000000000000000

    def _ja2int(self, number):
        """日本語の数詞を数値に変換"""
        result = 0
        digits = 0 # "1234"のようにな数字の連続
        thousands = 0 # 十, 百, 千 など
        for char in number:
            digit = self._num_dic.get(char, 0)
            if digit < 10:
                digits = digits * 10 + digit
            elif digit < 10000:
                if digits == 0:
                    digits = 1
                thousands += digits * digit
                digits = 0
            else:
                if digits == 0 and thousands == 0:
                    digits = 1
                result += (digits+thousands)*digit
                digits = 0
                thousands = 0
        return result + thousands + digits

    def _translate_int(self, number):
        """数字をグロンギ語に変換"""
        if number <= 9:
            return self._gr_numbers[number]

        result = []
        prefix = []
        while number != 0:
            fig = number % 9
            number = int(number/9)
            if fig == 1:
                if len(prefix) == 0:
                    result.append(self._gr_numbers[1])
                else:
                    result.append(u'グ'.join(prefix))
            elif fig > 1:
                result.append(u'グ'.join(prefix+[self._gr_numbers[fig]]))
            prefix.append(self._gr_numbers[9])
        return u'ド'.join(reversed(result))

    _re_ja_numbers = re.compile(u'[0123456789０１２３４５６７８９〇一二三四五六七八九零壱弐参十百千万億兆京]+')
    def translate(self, text):
        "日本語からグロンギ語への翻訳を行う"
        text = encodeMeCab(text)
        text = decodeMeCab(self._totagger.parse(text)).strip('\r\n')
        text = self.re_ltu.sub(u'\\1\\1', text)
        text = self.re_long.sub(u'\\1\\1', text) # 長音の変換
        text = self._re_ja_numbers.sub(
            lambda m: self._translate_int(self._ja2int(m.group())), text)
        return text

    re_numbers = re.compile(u'[0-9]+([+*✕][0-9]+)*')
    def _translate_num(self, number):
        "グロンギ語の数字を翻訳する"
        result = 0
        for term in number.split(u'+'):
            term_val = 1
            for num in term.split(u'✕'):
                term_val *= int(num)
            result += term_val
        return str(result)

    def grtranslate(self, text):
        "グロンギ語を日本語に翻訳する"
        text = encodeMeCab(text)
        text = decodeMeCab(self._fromtagger.parse(text)).strip('\r\n')
        text = self.re_numbers.sub(lambda m: self._translate_num(m.group()), text)
        return text
