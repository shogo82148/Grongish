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

## インストール

自動インストールは用意していないので手動で行う必要があります。
Pythonから見える場所にコピーしてご利用下さい。

## 辞書のコンパイル

レポジトリからCloneしてきた場合は辞書のコンパイルが必要です。

``` bash
$ git clone --recursive git@github.com:shogo82148/Grongish.git
$ make all
```

## ライセンス

プログラム本体はMITライセンスで提供します。詳しくはLICENCEを参照してください。
辞書ファイルにはIPAdicおよびOpen source mozc dictionaryを利用しています。
それぞれのライセンスを確認してください。

- [IPAdic](https://github.com/taku910/mecab/blob/32041d9504d11683ef80a6556173ff43f79d1268/mecab-ipadic/COPYING)
- [Open source mozc dictionary](https://github.com/google/mozc/tree/57110764ff7c0e0d930432b3dc4fd5ffec8e2f8b/src/data/dictionary_oss)
