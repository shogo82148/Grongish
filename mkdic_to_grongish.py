#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
グロンギ語への変換辞書を作成するスクリプト
"""

import csv
import re
import glob
import os.path

def make_dic():
    """
    日本語の読みからグロンギ語の読みへの変換辞書を作成
    """
    ja_list = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモワダヂヅデドバビブベボパピプペポラリルレロ'
    gr_list = 'ガギグゲゴバビブベボガギグゲゴダヂヅデドバビブベボザジズゼゾラリルレロパザジズゼゾダヂヅデドマミムメモサシスセソ'
    dic = {}
    for ja_char, gr_char in zip(ja_list, gr_list):
        dic[ja_char] = gr_char
    dic[u'ヤ'] = u'ジャ'
    dic[u'ユ'] = u'ジュ'
    dic[u'ヨ'] = u'ジョ'
    return dic
DIC = make_dic()

def to_grongish(csvinput, csvoutput):
    """
    ipadicの読み情報をグロンギ語に書き換える
    """
    fin = open(csvinput, 'r', encoding='eucjp', newline='')
    reader = csv.reader(fin)
    fout = open(csvoutput, 'w', encoding='utf-8', newline='')
    writer = csv.writer(fout, lineterminator="\n")
    re_long = re.compile(u'(.[ャュョァィゥェォ]?)ー')

    for row in reader:
        newrow = row[:4] # 表層表現,左文脈ID,右文脈ID,コスト
        yomi = row[11]
        if row[4] == '助詞':
            if yomi == 'ガ':
                yomi = 'グ'
            elif yomi == 'ノ':
                yomi = 'ン'
            elif yomi == 'ハ':
                yomi = 'パ'
            elif yomi == 'ヲ':
                yomi = 'ゾ'
        if row[4] == '連体詞':
            if yomi == 'コノ':
                yomi = 'ボン'
            elif yomi == 'ソノ':
                yomi = 'ゴン'
            elif yomi == 'アノ':
                yomi = 'ガン'
            elif yomi == 'ドノ':
                yomi = 'ゾン'
        yomi = ''.join((DIC.get(ch, ch) for ch in yomi))
        yomi = re_long.sub(u'\\1\\1', yomi) # 長音の変換
        # 拗音についてはMeCabでの解析後にやる
        writer.writerow(newrow + [yomi])

    fin.close()
    fout.close()

def convert_utf8(infile, outfile):
    """
    utf8にファイル変換を行う
    """
    fin = open(infile, 'r', encoding='eucjp')
    fout = open(outfile, 'w', encoding='utf-8')
    for line in fin:
        fout.write(line)
    fin.close()
    fout.close()

def main():
    """
    メインの処理
    """
    for csvinput in glob.iglob("./mecab/mecab-ipadic/*.csv"):
        basename = os.path.basename(csvinput)
        if basename == "Noun.number.csv":
            continue # 数字は別途処理
        csvoutput = "togrongishdic/" + basename
        to_grongish(csvinput, csvoutput)
    convert_utf8("./mecab/mecab-ipadic/left-id.def", "togrongishdic/left-id.def")
    convert_utf8("./mecab/mecab-ipadic/right-id.def", "togrongishdic/right-id.def")
    convert_utf8("./mecab/mecab-ipadic/matrix.def", "togrongishdic/matrix.def")

if __name__ == '__main__':
    main()
