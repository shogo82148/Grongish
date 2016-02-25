#!/usr/bin/env python
# -*- coding:utf-8 -*-
# an example of Grangish translate server

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import GrongishTranslator
g = GrongishTranslator.GrongishTranslator(dic='grongishdic')

grongishChars = set(u'ガギグゲゴザジズゼゾダヂヅデドバビブベボラリルレロサシスセソマミムメモパジャュョン')

def translateTo(request):
    text = request.params.get('text') or ''
    nbest = max(int(request.params.get('nbest') or '1'), 1)
    retranslation = request.params.get('retranslation')
    fromLang = (request.params.get('from') or 'auto').lower()

    # auto detect the language of text
    if fromLang == 'auto':
        all_length = len(text)
        d_length = len([ch for ch in text if ch in grongishChars])
        if all_length == 0:
            fromLang = "ja"
        elif float(d_length)/all_length>=0.7:
            fromLang = "grongish"
        else:
            fromLang = "ja"

    if fromLang == "ja" or fromLang == "ja_jp" or fromLang == "ja-jp" or fromLang == "japanese":
        translated = g.translate(text)
        result = {
            "original": text,
            "translated": [translated],
            "lang": "ja",
        }
        if retranslation:
            result["retransled"] = g.grtranslateNBest(translated, nbest)
    elif fromLang == "grongish":
        translated = g.grtranslateNBest(text, nbest)
        result = {
            "original": text,
            "translated": translated,
            "lang": "grongish",
        }
        if retranslation:
            result["retranslated"] = g.translate(translated[0])
    else:
        result = {
            "error": "unsuppoted language"
        }

    return result

def translateFrom(request):
    return {"result": g.grtranslateNBest(text, nbest)}

config = Configurator()
config.add_route('translate', '/translate')
config.add_view(translateTo, route_name='translate', renderer='json')
application = config.make_wsgi_app()

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8080, application)
    server.serve_forever()
