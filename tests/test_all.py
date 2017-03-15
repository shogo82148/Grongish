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
