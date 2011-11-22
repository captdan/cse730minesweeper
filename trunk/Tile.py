import random

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

    
