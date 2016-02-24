グロンギ語変換スクリプト
======================
日本語とグロンギ語の相互翻訳を行うスクリプトです。

## 使い方

    from GrongishTranslator import GrongishTranslator
    g = GrongishTranslator(dic='/PATH/TO/GrongishTranslator/grongishdic')
    
    print g.translate(u'お前のにおいがリントどもを誘ったのだ')
    # ゴラゲンビゴギグリントゾロゾガゴダダボザ
    
    print g.grtranslate(u'ゴラゲンビゴギグリントゾロゾガゴダダボザ')
    # お前のにおいがリントどもを誘ったのだ

## 必要なもの

- [MeCab](http://taku910.github.io/mecab/)
- MeCabのPythonバインディング
- [jcconv](https://pypi.python.org/pypi/jcconv)

## インストール

自動インストールは用意していないので手動で行う必要があります。
Pythonから見える場所にコピーしてご利用下さい。

## 辞書のコンパイル

レポジトリからCloneしてきた場合は辞書のコンパイルが必要です。

``` bash
$ git clone --recursive git@github.com:shogo82148/Grongish.git
$ cd Grongish
$ python mkdic.py
$ cd grongishdic
$ /usr/local/libexec/mecab/mecab-dict-index
```

## ライセンス
COPYING を参照
