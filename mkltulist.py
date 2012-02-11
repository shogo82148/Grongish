#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys
import re
import jcconv
from GrongishTranslator import GrongishTranslator

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def load_matrix(right_ids):
    matrix = {}
    for i in right_ids:
        matrix[i] = []

    f = open('matrix.def')
    for line in f:
        items = line.strip().split()
        if len(items)<3:
            continue
        if items[0] not in right_ids:
            continue
        matrix[items[0]].append((int(items[2]), items[1]))
    return matrix

def main():
    max_cost = 10000

    #「っ」で終わる単語のright-idを記録
    print >>sys.stderr, u'Finds right-id'
    ids_filename = sys.argv[1]
    f = codecs.open(ids_filename, 'r', 'utf-8')
    right_ids = set()
    for line in f:
        word = line.rstrip('\r\n').split(',')
        #最後が「っ」で終わっていないものは無視
        if not word[0].endswith(u'っ'):
            continue

        #right-idを記録
        right_ids.add(word[2])
    f.close()

    #「っ」の次に来るleft-idを探す
    print >>sys.stderr, u'Finds left-id'
    m = load_matrix(right_ids)
    left_ids = set()
    for right_id in right_ids:
        m[right_id].sort()
        for cost, left_id in m[right_id]:
            if cost>=max_cost:
                break
            left_ids.add(left_id)

    #left_idを持つ単語の先頭の文字を取得
    print >>sys.stderr, u'Finds start characters'
    start_chars = dict([(left_id, set()) for left_id in left_ids])
    f = codecs.open(ids_filename, 'r', 'utf-8')
    re_start = re.compile(u'([あ-ん][ゃゅょぁぃぅぇぉ]?)')
    for line in f:
        word = line.rstrip('\r\n').split(',')
        left_id = word[1]
        if left_id not in left_ids:
            continue
        res = re_start.match(word[0])
        if res:
            start_chars[left_id].add(res.group())
    f.close()

    #表示
    for right_id in right_ids:
        char_set = set()
        for cost, left_id in m[right_id]:
            if cost>=max_cost:
                break
            for char in start_chars[left_id]:
                char_set.add(char)
        print right_id, " ".join(char_set)

if __name__=='__main__':
    main()

