#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys
import jcconv
from GrongishTranslator import GrongishTranslator
import re
import glob
import zlib
INVALID_COST = 30000
LIMIT = 10000

class Matrix(object):
    def __init__(self):
        self.mat = {}
        self.right_size = 0
        self.left_size = 0

    def open_mozc(self, filename):
        f = open(filename, 'r')
        content = zlib.decompress(f.read()).split('\n')
        f.close()

        mat = {}
        pos_size = int(content[0]) # The first line contains the matrix column/row size.
        for array_index, line in enumerate(content[1:]):
            if line == '':
                continue
            cost = int(line)
            rid = array_index / pos_size
            lid = array_index % pos_size
            if rid == 0 and lid == 0:
                cost = 0
            mat[(rid, lid)] = cost
        self.mat = mat
        self.right_size = pos_size
        self.left_size = pos_size

    def get(self, right_id, left_id):
        return self.mat.get((right_id, left_id), INVALID_COST)

    def set(self, right_id, left_id, cost):
        self.mat[(right_id, left_id)] = cost
        if right_id>=self.right_size:
            self.right_size = right_id+1
        if left_id>=self.left_size:
            self.left_size = left_id+1

    def write(self, filename):
        f = codecs.open(filename, 'w', 'utf-8')
        f.write('%d %d\n' % (self.right_size, self.left_size))
        for right_id in xrange(self.right_size):
            for left_id in xrange(self.left_size):
                f.write('%d %d %d\n' % (right_id, left_id, self.get(right_id, left_id)))
        f.close()

class FeatureIDs(list):
    def open_mozc(self, filename):
        f = codecs.open(filename, 'r', 'utf-8')
        for line in f:
            columns = line.strip().split()
            self.append(columns[1])

    def write(self, filename):
        f = codecs.open(filename, 'w', 'utf-8')
        for i, feature in enumerate(self):
            f.write('%d %s\n' % (i, feature))

class WordDic(list):
    def read_mozc(self, filename):
        f = codecs.open(filename, 'r', 'utf-8')
        for line in f:
            word = line.rstrip('\r\n').split('\t', 5)
            surface = word[0]
            left_id = int(word[1])
            right_id = int(word[2])
            cost = int(word[3])
            feature = word[4]
            self.append([surface, left_id, right_id, cost, feature])

class Dic(object):
    re_start = re.compile(u'([ア-ン][ャュョァィゥェォ]?)')
    def open_mozc_dic(self, dic):
        self.words = WordDic()
        for word_file in sorted(glob.glob(dic + '/dictionary[0-9][0-9].txt')):
            print >>sys.stderr, 'Loading ' + word_file
            self.words.read_mozc(word_file)

        print >>sys.stderr, 'Loading matrix...'
        self.mtx = Matrix()
        self.mtx.open_mozc(dic + '/connection.deflate')

        print >>sys.stderr, 'Loading right-id...'
        self.right_ids = FeatureIDs()
        self.right_ids.open_mozc(dic + '/id.def')

        print >>sys.stderr, 'Loading left-id...'
        self.left_ids = FeatureIDs()
        self.left_ids.open_mozc(dic + '/id.def')

    def to_grongish(self):
        g = GrongishTranslator()
        words = self.words
        right_ids = self.right_ids
        print >>sys.stderr, 'To Grongish...'
        for i in xrange(len(words)):
            if i%1000==0:
                print >>sys.stderr, '%d...\r' % i,
            word = words[i]
            feature = right_ids[word[2]].split(',')
            yomi = g.translate(word[-1])
            word[0] = yomi

    def build_new_ids(self):
        print >>sys.stderr, 'Making new ids...'
        endsltu_right_ids = set()
        first_char = [set() for i in self.left_ids]
        re_start = self.re_start
        for surface, left_id, right_id, cost, feature in self.words:
            #「っ」で終わる単語のright-idを検索
            if surface.endswith(u'ッ'):
                endsltu_right_ids.add(right_id)

            #left_idごとに先頭の文字を集計
            m = re_start.match(surface)
            if m:
                first_char[left_id].add(m.group())

        #隣接可能なidの組みを列挙
        mtx = self.mtx
        next_left_ids = set()
        possible_pair = {}
        for right_id in endsltu_right_ids:
            l = []
            for left_id in xrange(mtx.left_size):
                if mtx.get(right_id, left_id)>=LIMIT:
                    continue
                next_left_ids.add(left_id)
                l.append(left_id)
            possible_pair[right_id] = l

        #新しいleft_idを作成
        ltu_left_ids = {}
        for left_id in next_left_ids:
            next_chars = list(first_char[left_id])
            next_chars.sort()
            d = {}
            feature = self.left_ids[left_id]
            if feature.startswith(u'名詞'):
                #Left-idが名詞の時は新しいidを作らない
                for next_char in next_chars:
                    d[next_char] = left_id
            elif len(next_chars)>0:
                self.left_ids[left_id] = feature + ',' + next_chars[0]
                d[next_chars[0]] = left_id
                for next_char in next_chars[1:]:
                    new_id = len(self.left_ids)
                    self.left_ids.append(feature + ',' + next_char)
                    d[next_char] = new_id
            else:
                d[''] = left_id
            ltu_left_ids[left_id] = d

        #新しいright_idを作成
        ltu_right_ids = {}
        for right_id, left_ids in possible_pair.iteritems():
            next_chars = set()
            for left_id in left_ids:
                if mtx.get(right_id, left_id)>=INVALID_COST:
                    continue
                for next_char in first_char[left_id]:
                    next_chars.add(next_char)
            d = {}
            feature = self.right_ids[right_id]
            next_chars = list(next_chars)
            next_chars.sort()
            for next_char in next_chars:
                new_id = len(self.right_ids)
                self.right_ids.append(feature + ',' + next_char)
                d[next_char] = new_id
            ltu_right_ids[right_id] = d

        self.possible_pair = possible_pair
        self.ltu_left_ids = ltu_left_ids
        self.ltu_right_ids = ltu_right_ids

    def build_new_matrix(self):
        print >>sys.stderr, 'Bulding new matrix'
        possible_pair = self.possible_pair
        ltu_left_ids = self.ltu_left_ids
        ltu_right_ids = self.ltu_right_ids
        mtx = self.mtx
        for right_id, left_id in mtx.mat.keys():
            cost = mtx.get(right_id, left_id)
            if left_id in ltu_left_ids:
                ids = ltu_left_ids[left_id]
                if right_id in ltu_right_ids:
                    for next_char, new_right_id in ltu_right_ids[right_id].iteritems():
                        if next_char not in ids:
                            continue
                        mtx.set(new_right_id, ids[next_char], cost)
                for next_char, new_left_id in ids.iteritems():
                    mtx.set(right_id, new_left_id, cost)

    def write(self, dic):
        print >>sys.stderr, 'Saving matrix...'
        self.mtx.write(dic + '/matrix.def')

        print >>sys.stderr, 'Saving right-id...'
        self.right_ids.write(dic + '/right-id.def')

        print >>sys.stderr, 'Saving left-id...'
        self.left_ids.write(dic + '/left-id.def')

        f = codecs.open(dic + '/dic.csv', 'w', 'utf-8')
        ltu_left_ids = self.ltu_left_ids
        ltu_right_ids = self.ltu_right_ids
        for surface, left_id, right_id, cost, feature in self.words:
            if left_id in ltu_left_ids:
                m = self.re_start.match(surface)
                if m:
                    left_id = ltu_left_ids[left_id][m.group()]
            if surface.endswith(u'ッ'):
                surface = surface[0:-1]
                for next_char, new_right_id in ltu_right_ids[right_id].iteritems():
                    f.write('%s%s,%d,%d,%d,%s\n' % (surface, next_char, left_id, new_right_id, cost, feature))
            else:
                f.write('%s,%d,%d,%d,%s\n' % (surface, left_id, right_id, cost, feature))

def main():
    dic = Dic()
    dic.open_mozc_dic('./mozc/src/data/dictionary_oss')
    dic.to_grongish()
    dic.build_new_ids()
    dic.build_new_matrix()
    dic.write('grongishdic')

if __name__=='__main__':
    main()

