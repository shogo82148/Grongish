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
