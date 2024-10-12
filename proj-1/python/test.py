import unittest

from nonoguru import *
from bench import *

OFFICIAL_EXAMPLE = ([[2,1],[2,1,3],[7],[1,3],[2,1]], [[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
OFFICIAL_SOLUTION = [[False, True, True, False, False], [False, True, True, False, True], [False, False, True, False, True], [False, True, True, True, False], [True, False, True, False, False], [True, False, True, False, False], [False, False, True, True, False], [False, True, False, True, False], [False, True, False, True, True], [True, True, False, False, False]]

class TestNonogram(unittest.TestCase):

    def do_test(self, input, output):
        bits = nonogram(*input, show = False)
        self.assertEqual(output, bits)

    def test_official(self):
        self.do_test(OFFICIAL_EXAMPLE, OFFICIAL_SOLUTION)

class TestWellPosed(unittest.TestCase):

    def test_official(self):
        self.assertTrue(well_posed(*OFFICIAL_EXAMPLE))

    def test_two_versions(self):
        """
        Compares two implementations for well posed
        """

        for i in range(100):
            input, output = random_test(5, 10)
            self.assertEqual(well_posed(*input), well_posed_2(*input))

class TestAllSolutions(unittest.TestCase):

    def test_official(self):
        self.assertEqual(all_solutions(*OFFICIAL_EXAMPLE), [OFFICIAL_SOLUTION])

    def test_two_versions(self):
        """
        Compares two implementations for all solutions
        """

        for i in range(100):
            input, output = random_test(5, 10)
            sols1 = all_solutions(*input)
            sols2 = all_solutions_2(*input)

            self.assertEqual(len(sols1), len(sols2))

            for sol in sols1:
                self.assertTrue(sol in sols2)

if __name__ == '__main__':
    unittest.main()
