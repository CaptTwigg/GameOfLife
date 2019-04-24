import numpy as np


class GOF:
    def __init__(self, cellState, overpopulation=3, underpopulation=2, reproduction=3):
        self.cellState = cellState
        self.overpopulation = overpopulation
        self.underpopulation = underpopulation
        self.reproduction = reproduction

    def rule(self, x, y):
        try:
            ADJACENTS = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)}
            surroundingCells = [self.cellState[x + dx][y + dy] for dy, dx in ADJACENTS
                                if 0 <= y + dy < len(self.cellState[0]) and 0 <= x + dx < len(self.cellState)]
            alive = surroundingCells.count(True)
            currentCell = self.cellState[x][y]

            if currentCell and alive > self.overpopulation:
                return False
            if currentCell and (alive == 2 or alive == self.reproduction):
                return True
            if currentCell and alive < self.underpopulation:
                return False
            if alive == self.reproduction:
                return True

        except IndexError:
            pass
            # print("asdf")
        return False

    def newCellState(self):
        return [[self.rule(x, y) for y in range(len(self.cellState[x]))] for x in range(len(self.cellState))]


if __name__ == "__main__":
    cell1 = [[False, False, False],
             [False, False, False],
             [False, False, False]]
    gof = GOF(cell1)

    print(gof.newCellState())
