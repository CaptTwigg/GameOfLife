class GOF:
    def __init__(self, cellState, overpopulation, underpopulation, reproduction):
        self.cellState = cellState
        self.overpopulation = overpopulation
        self.underpopulation = underpopulation
        self.reproduction = reproduction

    def rule(self, x, y):

        try:
            ADJACENTS = {(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)}
            # surroundingCells = [self.cellState[x - 1][y],  # left cell
            #                     self.cellState[x - 1][y - 1],  # top left
            #                     self.cellState[x][y - 1],  # Top cell
            #                     self.cellState[x + 1][y - 1],  # Top right
            #                     self.cellState[x + 1][y],  # Right cell
            #                     self.cellState[x + 1][y + 1],  # bottom right
            #                     self.cellState[x][y + 1],  # bottom cell
            #                     self.cellState[x - 1][y + 1],  # Right cell
            #                     ]
            surroundingCells = []

            for dy, dx in ADJACENTS:
                if 0 <= y + dy < len(self.cellState[0]) and 0 <= x + dx < len(self.cellState):
                    surroundingCells.append(self.cellState[x + dx][y + dy])
            alive = surroundingCells.count(True)
            current = self.cellState[x][y]

            # if alive > self.overpopulation:
            #     return False
            # if current is False and alive == self.reproduction:
            #     return True
            # if current and (alive == 2 or alive == self.reproduction):
            #     return True
            # if alive < self.underpopulation:
            #     return False

            if current and alive > self.overpopulation:
                return False
            if current and (alive == 2 or alive == self.reproduction):
                return True
            if current and alive < self.underpopulation:
                return False
            if alive == self.reproduction:
                return True

            # if alive > self.overpopulation:
            #     return False
            # if alive < self.underpopulation:
            #     return False
            # if alive == self.reproduction  or alive == 2:
            #     return True
            #print(x, y, alive, surroundingCells)

        except IndexError:
            pass
            print("asdf")
        return False

    def newCellState(self):
        cellState = []
        for x in range(len(self.cellState)):
            xCells = []
            for y in range(len(self.cellState[x])):
                xCells.append(self.rule(x, y))
            cellState.append(xCells)
        # print(cellState)
        return cellState
