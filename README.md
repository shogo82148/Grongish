グロンギ語変換スクリプト
======================
日本語とグロンギ語の相互翻訳を行うスクリプトです。

    from GrongishTranslator import GrongishTranslator
    g = GrongishTranslator(dic='.')
    
    print g.translate(u'お前のにおいがリントどもを誘ったのだ')
    # ゴラゲンビゴギグリントゾロゾガゴダダボザ
    
    print g.grtranslate(u'ゴラゲンビゴギグリントゾロゾガゴダダボザ')
    # お前のにおいがリントどもを誘ったのだ

## ライセンス
COPYING を参照
