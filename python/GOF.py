import numpy as np


class GOF:
    def __init__(self, cellState, aliveList, deadList):
        self.cellState = cellState
        self.aliveList = aliveList
        self.deadList = deadList

    def rule(self, x, y):
        try:
            ADJACENTS = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)}
            surroundingCells = [self.cellState[x + dx][y + dy] for dy, dx in ADJACENTS
                                if 0 <= y + dy < len(self.cellState[0]) and 0 <= x + dx < len(self.cellState)]
            alive = surroundingCells.count(True)
            currentCell = self.cellState[x][y]

            if currentCell and alive in self.aliveList:
                return True
            if alive in self.deadList:
                return True

        except IndexError:
            pass
            print("asdf")
        return False

    def newCellState(self):
        return [[self.rule(x, y) for y in range(len(self.cellState[x]))] for x in range(len(self.cellState))]


if __name__ == "__main__":
    cell1 = [[False, False, False],
             [False, False, False],
             [False, False, False]]
    gof = GOF(cell1)

    print(gof.newCellState())
