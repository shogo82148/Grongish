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

_ja_dic = (u'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモワ'
           u'ダヂヅデドバビブベボパピプペポラリルレロ')
_gr_dic = (u'ガギグゲゴバビブベボガギグゲゴダヂヅデドバビブベボザジズゼゾラリルレロパ'
           u'ザジズゼゾダヂヅデドマミムメモサシスセソ')
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

class GrongishTranslator(object):
    re_ltu = re.compile(u'ッ(.[ャュョァィゥェォ]?)')
    re_long = re.compile(u'(.[ャュョァィゥェォ]?)ー')
    def __init__(self, fromdic=None, todic=None):
        self._totagger = None
        if todic:
            self._totagger = MeCab.Tagger('-d%s -r%s/dicrc -Oyomi' % (todic, todic))

        self._num_dic = dict([(ch, i%10) for i, ch in enumerate(_numbers)])
        self._num_dic[u'十'] = 10
        self._num_dic[u'百'] = 100
        self._num_dic[u'千'] = 1000
        self._num_dic[u'万'] = 10000
        self._num_dic[u'億'] = 100000000
        self._num_dic[u'兆'] = 1000000000000
        self._num_dic[u'京'] = 10000000000000000

    def _ja2int(self, number):
        """日本語の数詞を数値に変換"""
        n1, n2, n3 = 0, 0, 0
        for c in number:
            digit = self._num_dic.get(c, 0)
            if digit < 10:
                n1 = n1 * 10 + digit
            elif digit < 10000:
                if n1 == 0:
                    n1 = 1
                n2 += n1 * digit
                n1 = 0
            else:
                if n1 == 0 and n2 == 0:
                    n1 = 1
                n3 += (n1+n2)*digit
                n1, n2 = 0, 0
        return n1+n2+n3

    def _translate_int(self, number):
        """数字をグロンギ語に変換"""
        if number <= 9:
            return _gr_numbers[number]

        result = []
        prefix = []
        while number != 0:
            fig = number % 9
            number = int(number/9)
            if fig == 1:
                if len(prefix) == 0:
                    result.append(_gr_numbers[1])
                else:
                    result.append(u'グ'.join(prefix))
            elif fig > 1:
                result.append(u'グ'.join(prefix+[_gr_numbers[fig]]))
            prefix.append(_gr_numbers[9])
        return u'ド'.join(reversed(result))

    def translate(self, text):
        text = encodeMeCab(text)
        text = decodeMeCab(self._totagger.parse(text)).strip('\r\n')
        text = self.re_ltu.sub(u'\\1\\1', text)
        text = self.re_long.sub(u'\\1\\1', text) # 長音の変換
        return text

    re_numbers = re.compile(r'[0-9]+([+*][0-9]+)*')
    def _translate_num(self, m):
        number = m.group()
        result = 0
        for term in number.split('+'):
            term_val = 1
            for num in term.split('*'):
                term_val *= int(num)
            result += term_val
        return str(result)

    def grtranslate(self, text):
        text = encodeMeCab(text)
        text = decodeMeCab(self._grtagger.parse(text)).strip('\r\n')
        text = self.re_numbers.sub(self._translate_num, text)
        return text
