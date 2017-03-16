# -*- coding:utf-8 -*-

"""
テスト
"""

import unittest
import GrongishTranslator

class TestGrongish(unittest.TestCase):
    """
    グロンギ語と日本語の相互変換のテスト
    """

    grongish = GrongishTranslator.GrongishTranslator(todic='togrongishdic')

    def test_ja2int(self):
        "日本語の数字表現を整数に変換するテスト"
        ja2int = self.grongish._ja2int
        self.assertEqual(ja2int(u'1'), 1)
        self.assertEqual(ja2int(u'2'), 2)
        self.assertEqual(ja2int(u'3'), 3)
        self.assertEqual(ja2int(u'4'), 4)
        self.assertEqual(ja2int(u'5'), 5)
        self.assertEqual(ja2int(u'6'), 6)
        self.assertEqual(ja2int(u'7'), 7)
        self.assertEqual(ja2int(u'8'), 8)
        self.assertEqual(ja2int(u'9'), 9)
        self.assertEqual(ja2int(u'10'), 10)
        self.assertEqual(ja2int(u'十'), 10)
        self.assertEqual(ja2int(u'11'), 11)
        self.assertEqual(ja2int(u'十一'), 11)
        self.assertEqual(ja2int(u'123'), 123)
        self.assertEqual(ja2int(u'百二十三'), 123)
        self.assertEqual(ja2int(u'1234'), 1234)
        self.assertEqual(ja2int(u'千二百三十四'), 1234)
        self.assertEqual(ja2int(u'1234万5678'), 12345678)
        self.assertEqual(ja2int(u'千二百三十四万五千六百七十八'), 12345678)

    def test_translate_int(self):
        """数字をグロンギ語に変換するテスト"""
        tr = self.grongish._translate_int
        self.assertEqual(tr(0), u'ゼゼソ')
        self.assertEqual(tr(1), u'パパン')
        self.assertEqual(tr(2), u'ドググ')
        self.assertEqual(tr(3), u'グシギ')
        self.assertEqual(tr(4), u'ズゴゴ')
        self.assertEqual(tr(5), u'ズガギ')
        self.assertEqual(tr(6), u'ギブグ')
        self.assertEqual(tr(7), u'ゲズン')
        self.assertEqual(tr(8), u'ゲギド')
        self.assertEqual(tr(9), u'バギン')
        self.assertEqual(tr(10), u'バギンドパパン')
        self.assertEqual(tr(11), u'バギンドドググ')
        self.assertEqual(tr(18), u'バギングドググ')

    def test_to_grongish(self):
        """
        グロンギ語への変換テスト
        """
        self.assertEqual(self.grongish.translate(u'殺してやる！'), u'ボソギデジャス！')
        self.assertEqual(self.grongish.translate(u'命拾いしたな'), u'ギボヂヂソギギダバ')
        self.assertEqual(self.grongish.translate(u'プレイヤー'), u'ムセギジャジャ')
        self.assertEqual(self.grongish.translate(u'やってやる'), u'ジャデデジャス')
        self.assertEqual(self.grongish.translate(u'これはクウガのベルト'), u'ボセパクウガンデスド')
        self.assertEqual(self.grongish.translate(u'この日遊戯を再開する'), u'ボンジジュグギゾガギバギグス')
        self.assertEqual(self.grongish.translate(u'ゲームの資格を持つのは誰だ'), u'ゲゲルンギバブゾロヅボパザセザ')
        self.assertEqual(self.grongish.translate(u'ゲームを始めるぞ'), u'ゲゲルゾザジレスゾ')
        self.assertEqual(self.grongish.translate(u'十八'), u'バギングドググ')
