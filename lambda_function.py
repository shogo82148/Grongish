# -*- coding:utf-8 -*-

import GrongishTranslator
g = GrongishTranslator.GrongishTranslator(dic='grongishdic')

GRONGISH_CHARS = set(u'ガギグゲゴザジズゼゾダヂヅデドバビブベボラリルレロサシスセソマミムメモパジャュョン')

def lambda_handler(event, context):
    text = event.get('text', '')
    nbest = max(int(event.get('nbest') or '1'), 1)
    retranslation = event.get('retranslation')
    from_lang = (event.get('from') or 'auto').lower()

    # auto detect the language of text
    if from_lang == 'auto':
        all_length = len(text)
        d_length = len([ch for ch in text if ch in GRONGISH_CHARS])
        if all_length == 0:
            from_lang = "ja"
        elif float(d_length)/all_length >= 0.7:
            from_lang = "grongish"
        else:
            from_lang = "ja"

    if from_lang == "ja" or from_lang == "ja_jp" or from_lang == "ja-jp" or from_lang == "japanese":
        translated = g.translate(text)
        result = {
            "original": text,
            "translated": [translated],
            "lang": "ja",
        }
        if retranslation:
            result["retranslated"] = g.grtranslateNBest(translated, nbest)
    elif from_lang == "grongish":
        translated = g.grtranslateNBest(text, nbest)
        result = {
            "original": text,
            "translated": translated,
            "lang": "grongish",
        }
        if retranslation:
            result["retranslated"] = [g.translate(translated[0])]
    else:
        result = {
            "error": "unsuppoted language"
        }

    return result
