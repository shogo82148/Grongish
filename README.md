グロンギ語変換スクリプト
======================
日本語とグロンギ語の相互翻訳を行うスクリプトです。

## インストール
自動インストールは用意していないので手動で行う必要があります。
あらかじめMeCabとPython-Bindingのインストールを行なっておいてください。
辞書のコンパイルが必要です。

    $ cd grongishdic
    $ /usr/local/libexec/mecab/mecab-dict-index

別途jcconvが必要です。easy_installやpipを使ってインストールしておいてください。

## 使い方

    from GrongishTranslator import GrongishTranslator
    g = GrongishTranslator(dic='grongishdic')
    
    print g.translate(u'お前のにおいがリントどもを誘ったのだ')
    # ゴラゲンビゴギグリントゾロゾガゴダダボザ
    
    print g.grtranslate(u'ゴラゲンビゴギグリントゾロゾガゴダダボザ')
    # お前のにおいがリントどもを誘ったのだ

## ライセンス
COPYING を参照
