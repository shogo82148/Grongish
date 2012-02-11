#!/usr/bin/env python
# -*- coding:utf-8 -*-
import MeCab
import jcconv
import itertools
import re

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
    re_long = re.compile(u'(.[ャュョァィゥェォ]?)ー')
    re_ltu = re.compile(u'ッ(.[ャュョァィゥェォ]?)')
    def __init__(self, tagger=None, dic=None):
        self._tagger = tagger or MeCab.Tagger()
        self._grtagger = None
        if dic:
            self._grtagger = MeCab.Tagger('-d %s -Oime' % dic)
        self._dic = self._mk_dic()
        self._num_dic = dict([(ch, i%10) for i,ch in enumerate(_numbers)])
        self._num_dic[u'十'] = 10
        self._num_dic[u'百'] = 100
        self._num_dic[u'千'] = 1000
        self._num_dic[u'万'] = 10000
        self._num_dic[u'億'] = 100000000
        self._num_dic[u'兆'] = 1000000000000
        self._num_dic[u'京'] = 10000000000000000

    def _mk_dic(self):
        dic = {}
        for ja, gr in itertools.izip(_ja_dic, _gr_dic):
            dic[ja] = gr
        dic[u'ヤ'] = u'ジャ'
        dic[u'ユ'] = u'ジュ'
        dic[u'ヨ'] = u'ジョ'
        return dic

    def _translate_node(self, surface, yomi, features):
        if features[0]==u'助詞':
            if yomi==u'ガ':
                return u'グ'
            elif yomi==u'ノ':
                return u'ン'
            elif yomi==u'ハ':
                return u'パ'
            elif yomi==u'ヲ':
                return u'ゾ'
        if yomi in (u'グロンギ', u'クウガ', u'リント', u'ゲゲル',
                    u'ゲリゼギバスゲゲル', u'グセパ', u'バグンダダ', u'ザギバスゲゲル'):
            return yomi
        return ''.join((self._dic.get(ch, ch) for ch in yomi))

    def _ja2int(self, number):
        """日本語の数詞を数値に変換"""
        n1, n2, n3 = 0,0,0
        for c in number:
            digit = self._num_dic.get(c, 0)
            if digit<10:
                n1 = n1*10 + digit
            elif digit<10000:
                if n1==0:
                    n1=1
                n2 += n1 * digit
                n1 = 0
            else:
                n3 += (n1+n2)*digit
                n1, n2 = 0, 0
        return n1+n2+n3

    def _translate_int(self, number):
        """数字をグロンギ語に変換"""
        if number<=9:
            return _gr_numbers[number]

        result = []
        prefix = []
        while number!=0:
            fig = number % 9
            number = int(number/9)
            if fig==1:
                if len(prefix)==0:
                    result.append(_gr_numbers[1])
                else:
                    result.append(u'グ'.join(prefix))
            elif fig>1:
                result.append(u'グ'.join(prefix+[_gr_numbers[fig]]))
            prefix.append(_gr_numbers[9])
        return u'ド'.join(reversed(result))

    def translate(self, text):
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        node = self._tagger.parseToNode(text)
        result = []
        while node:
            if node.stat>=2:
                node = node.next
                continue
            surface = node.surface.decode(u'utf-8')
            yomi = surface
            features = node.feature.decode('utf-8').split(',')
            if node.stat==0:
                yomi = features[7]
            yomi = jcconv.hira2kata(yomi)
            if features[1]==u'数':
                number = u''
                while True:
                    surface = node.surface.decode(u'utf-8')
                    features = node.feature.decode('utf-8').split(',')
                    if features[1]!=u'数':
                        break
                    number += surface
                    node = node.next
                number = self._ja2int(number)
                result.append(self._translate_int(number))
            else:
                result.append(self._translate_node(surface, yomi, features))
                node = node.next

        #長音と促音を変換
        text = u''.join(result)
        text = self.re_long.sub(u'\\1\\1', text)
        text = self.re_ltu.sub(u'\\1\\1', text)
        return text

    re_numbers = re.compile(r'[0-9*+]+')
    def grtranslate(self, text):
        def translate_num(m):
            number = m.group()
            result = 0
            for term in number.split('+'):
                term_val = 1
                for num in term.split('*'):
                    term_val *= int(num)
                result += term_val
            return str(result)

        if isinstance(text, unicode):
            text = text.encode('utf-8')
        text = self._grtagger.parse(text).decode('utf-8').strip('\r\n')
        text = self.re_numbers.sub(translate_num, text)
        return text

def main():
    g = GrongishTranslator(dic='.')
    test_text = [
        u'殺してやる！',
        u'命拾いしたな',
        u'プレイヤー',
        u'やってやる',
        u'これはクウガのベルト',
        u'本当に裏切ったんですか！？',
        u'0,1,2,3,4,5,6,7,8,9,10,20,300',
        u'日本語とグロンギ語の相互翻訳機能を追加しました。ぜひ、試してみてください。',
        ]
    for text in test_text:
        print text
        gr = g.translate(text)
        print gr
        print g.grtranslate(gr)
        print

if __name__=='__main__':
    main()
