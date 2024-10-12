import unittest

from nonoguru import *
from bench import *

OFFICIAL_EXAMPLE = ([[2,1],[2,1,3],[7],[1,3],[2,1]], [[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
OFFICIAL_SOLUTION = [[False, True, True, False, False], [False, True, True, False, True], [False, False, True, False, True], [False, True, True, True, False], [True, False, True, False, False], [True, False, True, False, False], [False, False, True, True, False], [False, True, False, True, False], [False, True, False, True, True], [True, True, False, False, False]]


TEST_1 = ([[1, 3, 2], [1, 1, 1, 1], [1, 2], [1, 1, 1, 1], [1, 2]], [[2, 1], [1], [2], [1, 1], [3], [1, 2], [1, 1], [1], [1], [1, 1]])
TEST_1_SOL = [[True, True, False, True, False], [False, False, False, False, True], [False, True, True, False, False], [True, False, False, True, False], [True, True, True, False, False], [True, False, True, True, False], [False, True, False, False, True], [False, False, False, False, True], [True, False, False, False, False], [True, False, False, True, False]]

TEST_2 = ([[1, 1], [2], [1, 1]], [[1, 1], [1], [2], [1]])
TEST_2_SOL = [[True, False, True], [False, True, False], [True, True, False], [False, False, True]]

class TestNonogram(unittest.TestCase):

    def do_test(self, input, output):
        bits = nonogram(*input, show = False, constraints_for_line = constraints_for_line_poly)
        self.assertEqual(output, bits)

    def test_official(self):
        self.do_test(OFFICIAL_EXAMPLE, OFFICIAL_SOLUTION)

    def custom_test_1(self):
        # FIXME: I think these are not well posed
        self.do_test(TEST_1, TEST_1_SOL)

    def custom_test_2(self):
        # FIXME: I think these are not well posed
        self.do_test(TEST_2, TEST_2_SOL)

    def test_random_poly(self):
        width, height = 3, 4
        for i in range(100):
            input, output = random_test(width, height)
            sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute),

            while len(sols) != 1:
                input, output = random_test(width, height)
                sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute),

            self.do_test(input, output)

class TestWellPosed(unittest.TestCase):

    def test_official(self):
        self.assertTrue(well_posed(*OFFICIAL_EXAMPLE))
        pass

    def test_two_versions(self):
        """
        Compares two implementations for well posed
        """

        for i in range(100):
            input, output = random_test(5, 10)
            self.assertEqual(
                well_posed(*input, constraints_for_line = constraints_for_line_brute),
                well_posed(*input, constraints_for_line = constraints_for_line_poly))

class TestAllSolutions(unittest.TestCase):

    def test_official(self):
        self.assertEqual(all_solutions(*OFFICIAL_EXAMPLE), [OFFICIAL_SOLUTION])

    def test_two_versions(self):
        """
        Compares two implementations for all solutions
        """

        for i in range(100):
            input, output = random_test(5, 10)
            sols1 = all_solutions(*input, constraints_for_line = constraints_for_line_brute)
            sols2 = all_solutions(*input, constraints_for_line = constraints_for_line_poly)

            self.assertEqual(len(sols1), len(sols2))

            for sol in sols1:
                self.assertTrue(sol in sols2)

if __name__ == '__main__':
    unittest.main()
