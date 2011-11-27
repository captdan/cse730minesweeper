import random

#Represents a single tile on a minesweeper board.
#Mostly just a nice container for data.

class Tile:
    
    def __init__(self):
        self.mine = False
        self.revealed = False
        self.displayNum = 0
        self.flagged = False

    def setDisplayNum(self, surroundingMines, errorChance):
        r = random.random()
        if r < errorChance:
            error = (-1) ** random.randint(0, 1)
        else:
            error = 0
        self.displayNum = surroundingMines + error
        self.displayNum = min(self.displayNum, 8)
        self.displayNum = max(self.displayNum, 0)

    def prettyPrintChar(self):
        if self.flagged:
            return 'F'
        elif not self.revealed:
            return 'X'
        elif self.mine:
            return 'M'
        else:
            return str(self.displayNum)
    def truePrintChar(self):
        if self.mine:
            return 'M'
        else:
            return str(displayNum)

    def reveal(self):
        self.revealed = True
        self.flagged = False

    def flag(self):
        self.flagged = True

    def unflag(self):
        self.flagged = False


