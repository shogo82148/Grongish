import unittest
import GrongishTranslator

class TestGrongish(unittest.TestCase):
    grongish = GrongishTranslator.GrongishTranslator(dic='togrongishdic')

    def test_add_three(self):
        self.assertEqual(7, 7)
