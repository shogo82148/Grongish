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
    dic['ヤ'] = 'ジャ'
    dic['ユ'] = 'ジュ'
    dic['ヨ'] = 'ジョ'
    dic['キャ'] = 'キャ'
    dic['キュ'] = 'キュ'
    dic['キョ'] = 'キョ'
    dic['チャ'] = 'ジャ'
    dic['チュ'] = 'ジュ'
    dic['チョ'] = 'ジョ'
    dic['ファ'] = 'ザ'
    dic['フィ'] = 'ジ'
    dic['フェ'] = 'ゼ'
    dic['フォ'] = 'ゾ'

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

    for row in reader:
        newrow = row[:4] # 表層表現,左文脈ID,右文脈ID,コスト
        yomi = _to_grongish(row[11])
        if row[4] == '助詞':
            if yomi == 'ガ':
                yomi = 'グ'
            elif yomi == 'ボ': #'ノ'
                yomi = 'ン'
            elif yomi == 'ザ': #'ハ'
                yomi = 'パ'
            elif yomi == 'ヲ':
                yomi = 'ゾ'
        if row[4] == '連体詞':
            if yomi == 'ボボ': # 'コノ'
                yomi = 'ボン'
            elif yomi == 'ゴボ': # 'ソノ'
                yomi = 'ゴン'
            elif yomi == 'ガボ': # 'アノ'
                yomi = 'ガン'
            elif yomi == 'ゾボ': # 'ドノ'
                yomi = 'ゾン'
        # 拗音についてはMeCabでの解析後にやる
        writer.writerow(newrow + [yomi])

    fin.close()
    fout.close()

def _to_grongish(yomi):
    """
    ipadicの読み情報をグロンギ語に書き換える
    """
    ret = ""
    while len(yomi) > 0:
        ch = yomi[0]
        if len(yomi) >= 2 and yomi[:2] in DIC:
            ch = yomi[:2]
        yomi = yomi[len(ch):]
        ret += DIC.get(ch, ch)

        # 長音の処理　同じ文字を繰り返す
        if len(yomi) > 0 and yomi[0] == 'ー':
            yomi = yomi[1:]
            ret += DIC.get(ch, ch)

    return ret

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

def write_fallback_dic(outfile):
    """
    辞書に項目がなかった場合のフォールバック
    """
    ja_hira_list = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもわだぢづでどばびぶべぼぱぴぷぺぽらりるれろ'
    ja_list = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモワダヂヅデドバビブベボパピプペポラリルレロ'
    gr_list = 'ガギグゲゴバビブベボガギグゲゴダヂヅデドバビブベボザジズゼゾラリルレロパザジズゼゾダヂヅデドマミムメモサシスセソ'

    fout = open(outfile, 'w', encoding='utf-8', newline='')
    writer = csv.writer(fout, lineterminator="\n")
    for from_char, to_char in zip(ja_list, gr_list):
        writer.writerow([from_char, 10, 10, 7000, to_char])
    for from_char, to_char in zip(ja_hira_list, gr_list):
        writer.writerow([from_char, 10, 10, 7000, to_char])
    for from_char, to_char in zip(ja_list, gr_list):
        writer.writerow([from_char + "ー", 10, 10, 6500, to_char + to_char])
    for from_char, to_char in zip(ja_hira_list, gr_list):
        writer.writerow([from_char + "ー", 10, 10, 6500, to_char + to_char])
    writer.writerow(["ヤ", 10, 10, 7000, "ジャ"])
    writer.writerow(["ユ", 10, 10, 7000, "ジュ"])
    writer.writerow(["ヨ", 10, 10, 7000, "ジョ"])
    writer.writerow(["や", 10, 10, 7000, "ジャ"])
    writer.writerow(["ゆ", 10, 10, 7000, "ジュ"])
    writer.writerow(["よ", 10, 10, 7000, "ジョ"])
    writer.writerow(["ヤー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["ユー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["ヨー", 10, 10, 6500, "ジョジョ"])
    writer.writerow(["やー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["ゆー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["よー", 10, 10, 6500, "ジョジョ"])

    # 拗音
    writer.writerow(["キャ", 10, 10, 6500, "キャ"])
    writer.writerow(["キュ", 10, 10, 6500, "キュ"])
    writer.writerow(["キョ", 10, 10, 6500, "キョ"])
    writer.writerow(["チャ", 10, 10, 6500, "ジャ"])
    writer.writerow(["チュ", 10, 10, 6500, "ジュ"])
    writer.writerow(["チョ", 10, 10, 6500, "ジョ"])
    writer.writerow(["ジャ", 10, 10, 6500, "ジャ"])
    writer.writerow(["ジュ", 10, 10, 6500, "ジュ"])
    writer.writerow(["ジョ", 10, 10, 6500, "ジョ"])
    writer.writerow(["ファ", 10, 10, 6500, "ザ"])
    writer.writerow(["フィ", 10, 10, 6500, "ジ"])
    writer.writerow(["フェ", 10, 10, 6500, "ゼ"])
    writer.writerow(["フォ", 10, 10, 6500, "ゾ"])

    # 拗音 + 長音
    writer.writerow(["キャー", 10, 10, 6500, "キャキャ"])
    writer.writerow(["キュー", 10, 10, 6500, "キュキャ"])
    writer.writerow(["キョー", 10, 10, 6500, "キョキョ"])
    writer.writerow(["チャー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["チュー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["チョー", 10, 10, 6500, "ジョジョ"])
    writer.writerow(["ジャー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["ジュー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["ジョー", 10, 10, 6500, "ジョジョ"])
    writer.writerow(["ファー", 10, 10, 6500, "ザザ"])
    writer.writerow(["フィー", 10, 10, 6500, "ジジ"])
    writer.writerow(["フェー", 10, 10, 6500, "ゼゼ"])
    writer.writerow(["フォー", 10, 10, 6500, "ゾゾ"])

    # 拗音(ひらがな)
    writer.writerow(["きゃ", 10, 10, 6500, "キャ"])
    writer.writerow(["きゅ", 10, 10, 6500, "キュ"])
    writer.writerow(["きょ", 10, 10, 6500, "キョ"])
    writer.writerow(["ちゃ", 10, 10, 6500, "ジャ"])
    writer.writerow(["ちゅ", 10, 10, 6500, "ジュ"])
    writer.writerow(["ちょ", 10, 10, 6500, "ジョ"])
    writer.writerow(["じゃ", 10, 10, 6500, "ジャ"])
    writer.writerow(["じゅ", 10, 10, 6500, "ジュ"])
    writer.writerow(["じょ", 10, 10, 6500, "ジョ"])
    writer.writerow(["ふぁ", 10, 10, 6500, "ザ"])
    writer.writerow(["ふぃ", 10, 10, 6500, "ジ"])
    writer.writerow(["ふぇ", 10, 10, 6500, "ゼ"])
    writer.writerow(["ふぉ", 10, 10, 6500, "ゾ"])

    # 拗音(ひらがな) + 長音
    writer.writerow(["きゃー", 10, 10, 6500, "キャキャ"])
    writer.writerow(["きゅー", 10, 10, 6500, "キュキュ"])
    writer.writerow(["きょー", 10, 10, 6500, "キョキョ"])
    writer.writerow(["ちゃー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["ちゅー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["ちょー", 10, 10, 6500, "ジョジョ"])
    writer.writerow(["じゃー", 10, 10, 6500, "ジャジャ"])
    writer.writerow(["じゅー", 10, 10, 6500, "ジュジュ"])
    writer.writerow(["じょー", 10, 10, 6500, "ジョジョ"])
    writer.writerow(["ふぁー", 10, 10, 6500, "ザザ"])
    writer.writerow(["ふぃー", 10, 10, 6500, "ジジ"])
    writer.writerow(["ふぇー", 10, 10, 6500, "ゼゼ"])
    writer.writerow(["ふぉー", 10, 10, 6500, "ゾゾ"])

    writer.writerow(["ー", 10, 10, 10000, "ー"])
    writer.writerow(["っ", 10, 10, 10000, "ッ"])
    writer.writerow(["ッ", 10, 10, 10000, "ッ"])
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
    write_fallback_dic("togrongishdic/fallback.csv")
    convert_utf8("./mecab/mecab-ipadic/left-id.def", "togrongishdic/left-id.def")
    convert_utf8("./mecab/mecab-ipadic/right-id.def", "togrongishdic/right-id.def")
    convert_utf8("./mecab/mecab-ipadic/matrix.def", "togrongishdic/matrix.def")

if __name__ == '__main__':
    main()
