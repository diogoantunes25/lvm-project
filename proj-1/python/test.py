import unittest

from nonoguru import *
from bench import *

OFFICIAL_EXAMPLE = ([[2,1],[2,1,3],[7],[1,3],[2,1]], [[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
OFFICIAL_SOLUTION = [[False, True, True, False, False], [False, True, True, False, True], [False, False, True, False, True], [False, True, True, True, False], [True, False, True, False, False], [True, False, True, False, False], [False, False, True, True, False], [False, True, False, True, False], [False, True, False, True, True], [True, True, False, False, False]]

TEST_1 = ([[1, 1], [1, 1], [1, 1], [2, 1], [1, 1, 2], [1]], [[1], [1], [5], [1], [2, 2], [1, 1]])
TEST_1_SOL = [[False, False, False, False, True, False], [False, False, False, True, False, False], [True, True, True, True, True, False], [False, False, False, False, False, True], [True, True, False, True, True, False], [False, False, True, False, True, False]]

TEST_2 = ([[1, 1], [1, 1, 1], [2, 1], [5], [2, 1], [1]], [[2, 1], [3], [1, 2], [1, 2], [1], [3, 1]])
TEST_2_SOL = [[False, False, True, True, False, True], [False, True, True, True, False, False], [True, False, False, True, True, False], [False, True, False, True, True, False], [False, False, False, True, False, False], [True, True, True, False, True, False]]

class TestNonogram(unittest.TestCase):

    def do_test_brute(self, input, output):
        bits = nonogram(*input, show = False, constraints_for_line = constraints_for_line_brute)
        self.assertEqual(output, bits)

    def do_test_poly(self, input, output):
        bits = nonogram(*input, show = False, constraints_for_line = constraints_for_line_poly)
        self.assertEqual(output, bits)

    def test_official(self):
        self.do_test_poly(OFFICIAL_EXAMPLE, OFFICIAL_SOLUTION)
        self.do_test_brute(OFFICIAL_EXAMPLE, OFFICIAL_SOLUTION)

    def test_random_brute(self):
        width, height = 3, 4
        for i in range(100):
            input, output = random_test(width, height)
            sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute)

            while len(sols) != 1:
                input, output = random_test(width, height)
                sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute)

            assert(well_posed(*input, constraints_for_line = constraints_for_line_brute))

            self.do_test_brute(input, output)

    def test_random_poly(self):
        width, height = 3, 4
        for i in range(100):
            input, output = random_test(width, height)
            sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute)

            while len(sols) != 1:
                input, output = random_test(width, height)
                sols = all_solutions(*input, constraints_for_line = constraints_for_line_brute)

            assert(well_posed(*input, constraints_for_line = constraints_for_line_brute))

            self.do_test_poly(input, output)

class TestWellPosed(unittest.TestCase):

    def test_official(self):
        self.assertTrue(well_posed(*OFFICIAL_EXAMPLE))

    def test_1(self):
        brute = well_posed(*TEST_1, constraints_for_line = constraints_for_line_brute)
        poly = well_posed(*TEST_1, constraints_for_line = constraints_for_line_poly)
        self.assertEqual(brute, poly)

    def test_two_versions(self):
        """
        Compares two implementations for well posed
        """

        for i in range(100):
            input, output = random_test(6, 6)
            brute = well_posed(*input, constraints_for_line = constraints_for_line_brute)
            poly = well_posed(*input, constraints_for_line = constraints_for_line_poly)

            if not (brute == poly):
                print(input)
                print(output)

            self.assertEqual(brute, poly)

class TestAllSolutions(unittest.TestCase):

    def test_official(self):
        self.assertEqual(all_solutions(*OFFICIAL_EXAMPLE), [OFFICIAL_SOLUTION])

    def do_compare(self, input):
        sols1 = all_solutions(*input, constraints_for_line = constraints_for_line_brute)
        sols2 = all_solutions(*input, constraints_for_line = constraints_for_line_poly)

        self.assertEqual(len(sols1), len(sols2))

        for sol in sols1:
            self.assertTrue(sol in sols2)

    def test_1(self):
        self.do_compare(TEST_1)

    def test_2(self):
        self.do_compare(TEST_2)

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
