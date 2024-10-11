import unittest
from nonoguru import *

OFFICIAL_EXAMPLE = ([[2,1],[2,1,3],[7],[1,3],[2,1]], [[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
OFFICIAL_SOLUTION = [[False, True, True, False, False], [False, True, True, False, True], [False, False, True, False, True], [False, True, True, True, False], [True, False, True, False, False], [True, False, True, False, False], [False, False, True, True, False], [False, True, False, True, False], [False, True, False, True, True], [True, True, False, False, False]]

class TestNonogram(unittest.TestCase):

    def test_official(self):
        bits = nonogram(*OFFICIAL_EXAMPLE, show = False)
        self.assertEqual(OFFICIAL_SOLUTION, bits)

class TestWellPosed(unittest.TestCase):

    def test_official(self):
        self.assertTrue(well_posed(*OFFICIAL_EXAMPLE))

if __name__ == '__main__':
    unittest.main()
