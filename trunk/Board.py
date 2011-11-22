from MineTile import MineTile
import random

class Board:
    
    #constructor
    def __init__(self, rows, columns, mines, errorChance):
        #create 2D array (list of lists) of MineTiles
        self.rows = rows
        self.columns = columns
        #empty array of length columns
        self.tiles = [None] * columns
        #fill each space in the array with an empty array of length rows
        for i in range(columns):
            self.tiles[i] = [None] * rows
            #fill each space in the array with a new MineTile
            for j in range(rows):
                self.tiles[i][j] = MineTile()
        #populate minefield
        mineLocations = random.sample(range(0, rows * columns) , mines) 
        for l in mineLocations:
            self.tiles[l / rows][l % rows].mine = True
        #set display numbers for each tile
        #for each tile in the board...
        for i in range(columns):
            for j in range(rows):
                #for each square surrounding the tile...
                #set a counter, add up the number of mines in the 3x3
                #square about the tile we are examining, and subtract the 
                #mine of the tile itself if it exists (probably overkill)
                c = 0 + (-1) * self.tiles[i][j].mine
                for k in range(max(i - 1, 0), min(i + 2, columns)):
                    for l in range(max(j - 1, 0), min(j + 2, rows)):
                        c += 1 * self.tiles[k][l].mine
                self.tiles[i][j].setDisplayNum(c, errorChance)
    
    #reveals the current tile
    #if it is a mine, return false
    #otherwise, sets it as revealed and returns true
    def reveal(self, x, y):
        if self.tiles[x][y].mine:
            return False
        else:
            self.tiles[x][y].revealed = True
            return True

    def flag(self, x, y):
        self.tiles[x][y].flagged = True

    def unflag(self, x, y):
        self.tiles[x][y].flagged = False
            
    def prettyPrint(self):
        s = ""
        for y in range(self.rows):
            for x in range(self.columns):          
                s += (str(self.tiles[x][y].displayNum) if self.tiles[x][y].revealed else ("F" if self.tiles[x][y].flagged else "X")) + " "
            s += '\n'
        return s

    def truePrint(self):
        s = ""
        for y in range(self.rows):
            for x in range(self.columns):
                s += "M " if self.tiles[x][y].mine else str(self.tiles[x][y].displayNum) + " "
            s += "\n"
        return s

    def incorrectFlags(self):
        return sum([[x.flagged and not x.mine for x in y].count(True) for y in self.tiles])
