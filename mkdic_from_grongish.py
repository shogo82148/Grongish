#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
グロンギ語から日本語への変換辞書を作成する
"""

import codecs
import sys
import glob
import zlib
import re
from GrongishTranslator import GrongishTranslator
INVALID_COST = 30000
LIMIT = 3000
WORD_LIMIT = 8000

class Matrix(object):
    """
    隣接コスト
    """
    def __init__(self):
        self.mat = {}
        self.right_size = 0
        self.left_size = 0

    def open_mozc(self, filename):
        """
        mozcの辞書の隣接コストファイルを開く
        """
        with open(filename, 'rb') as fmat:
            content = zlib.decompress(fmat.read()).decode('utf-8').split('\n')

        mat = {}
        pos_size = int(content[0]) # The first line contains the matrix column/row size.
        for array_index, line in enumerate(content[1:]):
            if line == '':
                continue
            cost = int(line)
            rid = array_index // pos_size
            lid = array_index % pos_size
            if rid == 0 and lid == 0:
                cost = 0
            mat[(rid, lid)] = cost
        self.mat = mat
        self.right_size = pos_size
        self.left_size = pos_size

    def get(self, right_id, left_id):
        """
        right_idとleft_idの隣接コストを取得する
        """
        return self.mat.get((right_id, left_id), INVALID_COST)

    def set(self, right_id, left_id, cost):
        """
        right_idとleft_idの隣接コストを設定する
        """
        self.mat[(right_id, left_id)] = cost
        if right_id >= self.right_size:
            self.right_size = right_id+1
        if left_id >= self.left_size:
            self.left_size = left_id+1

    def write(self, filename):
        """
        filenameに隣接コストを書き込む
        """
        fmat = codecs.open(filename, 'w', 'utf-8')
        fmat.write('%d %d\n' % (self.right_size, self.left_size))
        for right_id in range(self.right_size):
            print('%d/%d...\r' % (right_id, self.right_size), file=sys.stderr, end='')
            for left_id in range(self.left_size):
                fmat.write('%d %d %d\n' % (right_id, left_id, self.get(right_id, left_id)))
        fmat.close()
        print('', file=sys.stderr)

class FeatureIDs(list):
    """
    素性IDリスト
    """
    def open_mozc(self, filename):
        """
        mozcの素性IDリストを開く
        """
        fids = codecs.open(filename, 'r', 'utf-8')
        for line in fids:
            columns = line.strip().split()
            self.append(columns[1])
        fids.close()

    def write(self, filename):
        """
        filenameに素性IDリストを保存する
        """
        fids = codecs.open(filename, 'w', 'utf-8')
        for i, feature in enumerate(self):
            fids.write('%d %s\n' % (i, feature))

class WordDic(list):
    """
    単語辞書
    """
    def read_mozc(self, filename):
        """
        mozcの単語辞書を開く
        """
        fdic = codecs.open(filename, 'r', 'utf-8')
        for line in fdic:
            word = line.rstrip('\r\n').split('\t', 5)
            surface = word[0]
            left_id = int(word[1])
            right_id = int(word[2])
            cost = int(word[3])
            feature = word[4]
            if cost > WORD_LIMIT:
                continue
            self.append([surface, left_id, right_id, cost, feature])

class Dic(object):
    """
    グロンギ語から日本語への変換辞書
    """
    re_start = re.compile(u'([ア-ン][ャュョァィゥェォ]?)')

    def __init__(self):
        self.words = WordDic()
        self.mtx = Matrix()
        self.right_ids = FeatureIDs()
        self.left_ids = FeatureIDs()
        self.possible_pair = None
        self.ltu_left_ids = None
        self.ltu_right_ids = None

    def open_mozc_dic(self, dic):
        """
        mozcの辞書を開く
        """

        for word_file in sorted(glob.glob(dic + '/dictionary[0-9][0-9].txt')):
            print('Loading ' + word_file, file=sys.stderr)
            self.words.read_mozc(word_file)

        print('Loading matrix...', file=sys.stderr)
        self.mtx.open_mozc(dic + '/connection.deflate')

        print('Loading right-id...', file=sys.stderr)
        self.right_ids.open_mozc(dic + '/id.def')

        print('Loading left-id...', file=sys.stderr)
        self.left_ids.open_mozc(dic + '/id.def')

    def to_grongish(self):
        """
        mozcの辞書のエントリをグロンギ語に変換する
        """
        grongish = GrongishTranslator(todic='togrongishdic')
        words = self.words
        print('To Grongish...', file=sys.stderr)
        for i, word in enumerate(words):
            if i%1000 == 0:
                print('%d/%d...\r' % (i, len(words)), file=sys.stderr, end='')

            feature = self.right_ids[word[1]].split(",")
            if len(word[-1]) == 1 and feature[0] == u"助詞":
                # 助詞の特殊処理
                if word[-1] == u'が':
                    yomi = u'グ'
                elif word[-1] == u'の':
                    yomi = u'ン'
                elif word[-1] == u'は':
                    yomi = u'パ'
                elif word[-1] == u'を':
                    yomi = u'ゾ'
            elif len(word[-1]) == 2 and feature[0] == u"連体詞":
                if word[-1] == 'この':
                    yomi = 'ボン'
                elif word[-1] == 'その':
                    yomi = 'ゴン'
                elif word[-1] == 'あの':
                    yomi = 'ガン'
                elif word[-1] == 'どの':
                    yomi = 'ゾン'
            else:
                # 複数単語で構成されている場合があるので、表層表現からグロンギ語の発音を推定する
                yomi = grongish.translate(word[-1])
            word[0] = yomi

    def build_new_ids(self):
        """
        品詞IDの追加を行う
        """
        print('Making new ids...', file=sys.stderr)
        endsltu_right_ids = set()
        first_char = [{} for i in self.left_ids]
        re_start = self.re_start
        words_count = 0
        for word in self.words:
            surface = word[0]
            left_id = word[1]
            right_id = word[2]
            #「っ」で終わる単語のright-idを検索
            if surface.endswith(u'ッ'):
                feature = self.left_ids[left_id]
                if feature.startswith(u'感動詞') or feature.startswith(u'接頭詞'):
                    # 数が多いので無視
                    word[0] = ''
                    continue
                endsltu_right_ids.add(right_id)
                words_count += 1

            #left_idごとに先頭の文字を集計
            match = re_start.match(surface)
            if match:
                first_char[left_id][match.group()] = first_char[left_id].get(match.group(), 0) + 1
        print(words_count, "words", len(endsltu_right_ids), "features detected.", file=sys.stderr)

        #隣接可能なidの組みを列挙
        mtx = self.mtx
        next_left_ids = set()
        possible_pair = {}
        for right_id in endsltu_right_ids:
            left_ids = []
            for left_id in range(mtx.left_size):
                if mtx.get(right_id, left_id) >= LIMIT:
                    continue
                next_left_ids.add(left_id)
                left_ids.append(left_id)
            possible_pair[right_id] = left_ids
        print(len(next_left_ids), "left_ids neet to extend.", file=sys.stderr)

        #新しいleft_idを作成
        ltu_left_ids = {}
        new_left_ids_count = 0
        for left_id in next_left_ids:
            chars = first_char[left_id]
            next_chars = list(chars.keys())
            if len(next_chars) > 5:
                next_chars.sort(
                    key=lambda next_char, ch=chars: ch.get(next_char, 0),
                    reverse=True,
                )
                next_chars = next_chars[:5]
            next_chars.sort()
            dic = {}
            feature = self.left_ids[left_id]
            if not feature.startswith(u'動詞') and not feature.startswith(u'形容詞'):
                # 動詞・形容詞以外は組み合わせが多すぎて辞書が巨大になるので、left_idの作成は行わない
                for next_char in next_chars:
                    dic[next_char] = left_id
            elif len(next_chars) > 0:
                self.left_ids[left_id] = feature + ',GrongishNextChar:' + next_chars[0]
                dic[next_chars[0]] = left_id
                for next_char in next_chars[1:]:
                    new_id = len(self.left_ids)
                    new_left_ids_count += 1
                    self.left_ids.append(feature + ',GrongishNextChar:' + next_char)
                    dic[next_char] = new_id
            else:
                dic[''] = left_id
            ltu_left_ids[left_id] = dic
        print(new_left_ids_count, "left_ids were created.", file=sys.stderr)

        #新しいright_idを作成
        ltu_right_ids = {}
        new_right_ids_count = 0
        for right_id, left_ids in possible_pair.items():
            next_chars = set()
            left_ids.sort(key=lambda left_id: mtx.get(right_id, left_id))
            if len(left_ids) > 5:
                left_ids = left_ids[:5]
            for left_id in left_ids:
                if mtx.get(right_id, left_id) >= INVALID_COST:
                    break
                for next_char in first_char[left_id]:
                    next_chars.add(next_char)
            dic = {}
            feature = self.right_ids[right_id]
            next_chars = list(next_chars)
            next_chars.sort()
            for next_char in next_chars:
                new_id = len(self.right_ids)
                new_right_ids_count += 1
                self.right_ids.append(feature + ',GrongishNextChar:' + next_char)
                dic[next_char] = new_id
            ltu_right_ids[right_id] = dic
        print(new_right_ids_count, "right_ids were created.", file=sys.stderr)

        self.possible_pair = possible_pair
        self.ltu_left_ids = ltu_left_ids
        self.ltu_right_ids = ltu_right_ids

    def build_numbers(self):
        "+ * 等の演算子を定義"
        left_id = len(self.left_ids)
        self.left_ids.append(u"名詞,数,演算子,*,*,*,*")
        right_id = len(self.right_ids)
        self.right_ids.append(u"名詞,数,演算子,*,*,*,*")
        self.words.append([u"ド", left_id, right_id, 1, u'+'])
        self.words.append([u"グ", left_id, right_id, 1, u'*'])
        for number_id in [1935, 1936]: # 数字の品詞ID
            cost = self.mtx.get(number_id, number_id)
            self.mtx.set(right_id, number_id, cost)
            self. mtx.set(number_id, left_id, cost)

    def build_new_matrix(self):
        """
        隣接行列の構築
        """
        print('Bulding new matrix', file=sys.stderr)
        ltu_left_ids = self.ltu_left_ids
        ltu_right_ids = self.ltu_right_ids
        mtx = self.mtx
        keys = list(mtx.mat.keys())
        for right_id, left_id in keys:
            cost = mtx.get(right_id, left_id)
            if left_id in ltu_left_ids:
                ids = ltu_left_ids[left_id]
                if right_id in ltu_right_ids:
                    for next_char, new_right_id in ltu_right_ids[right_id].items():
                        if next_char not in ids:
                            continue
                        mtx.set(new_right_id, ids[next_char], cost)
                for next_char, new_left_id in ids.items():
                    mtx.set(right_id, new_left_id, cost)

    def write(self, dic):
        """
        辞書をファイルに保存する
        """
        print('Saving matrix...', file=sys.stderr)
        self.mtx.write(dic + '/matrix.def')

        print('Saving right-id...', file=sys.stderr)
        self.right_ids.write(dic + '/right-id.def')

        print('Saving left-id...', file=sys.stderr)
        self.left_ids.write(dic + '/left-id.def')

        fdic = codecs.open(dic + '/dic.csv', 'w', 'utf-8')
        ltu_left_ids = self.ltu_left_ids
        ltu_right_ids = self.ltu_right_ids
        for surface, left_id, right_id, cost, feature in self.words:
            if surface == "" or surface == ",":
                continue
            if left_id in ltu_left_ids:
                match = self.re_start.match(surface)
                if match:
                    if match.group() in ltu_left_ids[left_id]:
                        left_id = ltu_left_ids[left_id][match.group()]
            if surface.endswith(u'ッ'):
                surface = surface[0:-1]
                for next_char, new_right_id in ltu_right_ids[right_id].items():
                    fdic.write('%s%s,%d,%d,%d,%s\n' % (
                        surface, next_char, left_id, new_right_id, cost, feature
                    ))
            else:
                fdic.write('%s,%d,%d,%d,%s\n' % (surface, left_id, right_id, cost, feature))
        fdic.close()

def main():
    """
    mozcの辞書を元に、
    グロンギ語から日本語への変換辞書を作成する
    """
    dic = Dic()
    dic.open_mozc_dic('./mozc/src/data/dictionary_oss')
    dic.to_grongish()
    dic.build_new_ids()
    dic.build_numbers()
    dic.build_new_matrix()
    dic.write('fromgrongishdic')

if __name__ == '__main__':
    main()
