#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys
import jcconv
from GrongishTranslator import GrongishTranslator

sys.stdin  = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

ltu_list = {}
def load_ltu_list(g):
    f = codecs.open('ltulist.txt', 'r', 'utf-8')
    for line in f:
        l = line.strip().split()
        ltu_list[l[0]] = set([
        ''.join((g._dic.get(ch, ch) for ch in jcconv.hira2kata(yomi)))
        for yomi in l[1:]
        ])

def read_id(filename):
    f = codecs.open(filename, 'r', 'utf-8')
    ids = {}
    for line in f:
        item_id, features = line.strip().split()
        ids[item_id] = features.split(',')
    return ids

def replace_ltu(word, features):
    yomi = word[0][:-1]
    for ltu in ltu_list[word[2]]:
        word[0] = yomi + ltu
        print ','.join(word)

def main():
    g = GrongishTranslator()
    load_ltu_list(g)
    right_ids = read_id('right-id.def')
    for line in sys.stdin:
        word = line.rstrip('\r\n').split(',')
        features = right_ids[word[2]]
        yomi = jcconv.hira2kata(word[0])
        yomi = g._translate_node(word[-1], yomi, features)
        yomi = g.re_long.sub(u'\\1\\1', yomi)
        yomi = g.re_ltu.sub(u'\\1\\1', yomi)
        word[0] = yomi
        if word[0][-1]==u'ッ':
            replace_ltu(word, features)
        else:
            print u','.join(word)

if __name__=='__main__':
    main()

