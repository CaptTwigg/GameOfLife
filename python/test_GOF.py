import unittest
from GOF import GOF


# The rules:
#    cell        neighbor    cell's next state
#    ---------   --------    -----------------
# 1. live        < 2         dead
# 2. live        2 or 3      live
# 3. live        > 3         dead
# 4. dead        3           live
class test_GOF(unittest.TestCase):
    def setUp(self):
        self.deadList = [3]  # dead become alive
        self.aliveList = [2, 3]  # alive lives on
        # patterns
        self.cell1 = [[False, False, False],
                      [False, False, False],
                      [False, False, False]]

        self.cell2 = [[True, False, False],
                      [True, False, False],
                      [False, False, False]]

        self.cell3 = [[True, True, False],
                      [True, False, False],
                      [False, False, True]]

        self.cell4 = [[False, True, False],
                      [True, True, True],
                      [False, True, False]]

        self.cell5 = [[True, True, True],
                      [True, True, True],
                      [True, True, True]]

    def test_all_false(self):
        self.gof = GOF(self.cell1, aliveList=self.aliveList, deadList=self.deadList)
        self.assertEqual(self.gof.rule(0, 0), False)
        self.assertEqual(self.gof.rule(1, 1), False)
        self.assertEqual(self.gof.rule(2, 2), False)

        self.assertEqual(self.gof.newCellState(), [[False, False, False],
                                                   [False, False, False],
                                                   [False, False, False]])

    def test_semi(self):
        self.gof = GOF(self.cell2, aliveList=self.aliveList, deadList=self.deadList)
        self.assertEqual(self.gof.rule(0, 0), False)
        self.assertEqual(self.gof.rule(1, 1), False)
        self.assertEqual(self.gof.rule(2, 2), False)
        self.assertEqual(self.gof.newCellState(), [[False, False, False],
                                                   [False, False, False],
                                                   [False, False, False]])

        self.gof = GOF(self.cell3, aliveList=self.aliveList, deadList=self.deadList)
        self.assertEqual(self.gof.rule(0, 0), True)
        self.assertEqual(self.gof.rule(1, 1), False)
        self.assertEqual(self.gof.rule(2, 2), False)
        self.assertEqual(self.gof.newCellState(), [[True, True, False],
                                                   [True, False, False],
                                                   [False, False, False]])

        self.gof = GOF(self.cell4, aliveList=self.aliveList, deadList=self.deadList)
        self.assertEqual(self.gof.rule(0, 0), True)
        self.assertEqual(self.gof.rule(1, 1), False)
        self.assertEqual(self.gof.rule(2, 2), True)
        self.assertEqual(self.gof.newCellState(), [[True, True, True],
                                                   [True, False, True],
                                                   [True, True, True]])

    def test_all_true(self):
        self.gof = GOF(self.cell5, aliveList=self.aliveList, deadList=self.deadList)
        self.assertEqual(self.gof.rule(0, 0), True)
        self.assertEqual(self.gof.rule(1, 1), False)
        self.assertEqual(self.gof.rule(2, 2), True)
        self.assertEqual(self.gof.newCellState(), [[True, False, True],
                                                   [False, False, False],
                                                   [True, False, True]])
