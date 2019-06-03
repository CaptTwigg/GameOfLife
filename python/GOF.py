import time

import numpy as np


class GOF:
    def __init__(self, cellState, aliveList, deadList):
        self.cellState = cellState
        self.aliveList = aliveList
        self.deadList = deadList

    def rule(self, x, y):

        ADJACENTS = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)}
        surrounding_cells = [self.cellState[x + dx][y + dy] for dy, dx in ADJACENTS
                            if 0 <= y + dy < len(self.cellState[0]) and 0 <= x + dx < len(self.cellState)]
        alive = surrounding_cells.count(True)
        current_cell = self.cellState[x][y]

        if current_cell and alive in self.aliveList:
            return True
        if alive in self.deadList:
            return True

        return False

    def newCellState(self):
        return [[self.rule(x, y) for y in range(len(self.cellState[x]))] for x in range(len(self.cellState))]


if __name__ == "__main__":
    cell1 = [[True, True, False],
             [True, False, False],
             [False, False, False]]
    cell1 = np.random.choice(a=[False, True], size=(100, 100))
    deadList = [3]  # dead become alive
    aliveList = [2, 3]  # alive lives on
    gof = GOF(cell1, aliveList, deadList)
    timer = 0
    for i in range(10):
        # gof = GOF(cell1, aliveList, deadList)
        # gof.cellState = np.random.choice(a=[False, True], size=(100, 100))
        t0 = time.time()
        gof.cellState = gof.newCellState()
        print(gof.cellState)
        timer += time.time() - t0
    print(timer)
