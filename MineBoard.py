#!/usr/bin/python

from numpy import *
import random

class MineBoard:
    "A class representing the mineboard needed for minesweeper."

    #Board Variables
    isRevealed = []
    boardValues = []
    difficulty = 0
    mines = 0
    rows = 0
    columns = 0

    #Difficulty is defined as such: Easy = 0, Intermediate = 1, Expert = 2
    #Easy is a 9x9 board with 10 mines. Intermediate is a 16x16 board with
    #40 mines. Expert is a 16x30 board with 99 mines.

    def __init__(self, difficulty):

        if difficulty == 0:
            self.rows = 9
            self.columns = 9
            self.mines = 10
            self.difficulty = 0
        elif difficulty == 1:
            self.rows = 16
            self.columns = 16
            self.mines = 40
            self.difficulty = 1
        elif difficulty == 2:
            self.rows = 16
            self.columns = 30
            self.mines = 99
            self.difficulty = 2
            
        self.boardValues = zeros([self.rows,self.columns])

        self.isRevealed = []
        for i in range(self.rows):
            self.isRevealed.append( [] )
            for j in range(self.columns):
                self.isRevealed[i].append(False)

        MineBoard.populateMineField(self)

#---------------------------------------------------------------------

    def populateMineField(self):

        #Zeros out the board in case repopulating an old board
        self.boardValues = zeros([self.rows,self.columns])

        #------------------------Beginner------------------------
        if self.difficulty == 0:
            self.mines = 10
            #Populating the field with mines
            for x in range(self.mines):
                temp = random.randrange(0,70)
                if temp < 9:
                    if self.boardValues[0][temp] == -1:
                        x = x-1
                    else:
                        self.boardValues[0][temp] = -1
                else:
                    rowIndex = temp/8
                    colIndex = temp%8
                    if self.boardValues[rowIndex][colIndex] == -1:
                        x = x-1
                    else:
                        self.boardValues[rowIndex][colIndex] = -1
            #Calculating surrounding mine values (non-boundary)
            for i in range(1,self.rows-1):
                for j in range(1,self.columns-1):
                    counter = 0
                    if self.boardValues[i-1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j+1] == -1:
                        counter = counter + 1

                    if self.boardValues[i][j] != -1:
                        self.boardValues[i][j] = counter

            #Calculating surrounding mine values (top boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[0][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[0][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i] == -1:
                    counter = counter + 1
                if self.boardValues[1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[0][i] != -1:
                    self.boardValues[0][i] = counter

            #Calculating surrounding mine values (left boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][1] == -1:
                    counter = counter + 1
                if self.boardValues[i][1] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][1] == -1:
                    counter = counter + 1

                if self.boardValues[i][0] != -1:
                    self.boardValues[i][0] = counter

            #Calculating surrounding mine values (right boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][self.columns-1] == -1:
                    counter = counter + 1
                if self.boardValues[i][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-1] == -1:
                    counter = counter + 1

                if self.boardValues[i][self.columns-1] != -1:
                    self.boardValues[i][self.columns-1] = counter

            #Calculating surrounding mine values (bottom boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[self.rows-2][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[self.rows-1][i] != -1:
                    self.boardValues[self.rows-1][i] = counter

            #Calculating the corner values
            counter = 0
            if self.boardValues[1][0] == -1:
                counter = counter + 1
            if self.boardValues[0][1] == -1:
                counter = counter + 1
            if self.boardValues[1][1] == -1:
                counter = counter + 1
            self.boardValues[0][0] = counter

            counter = 0
            if self.boardValues[0][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-1] == -1:
                counter = counter + 1
            self.boardValues[0][self.columns-1] = counter

            counter = 0
            if self.boardValues[self.rows-2][0] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][1] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][0] = counter

            counter = 0
            if self.boardValues[self.rows-2][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][self.columns-1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][self.columns-2] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][self.columns-1] = counter


        #------------------------Intermediate------------------------
                    
        elif self.difficulty == 1:
            self.mines = 40
            #Populating the field with mines
            for x in range(self.mines):
                temp = random.randrange(0,235)
                if temp < 16:
                    if self.boardValues[0][temp] == -1:
                        x = x-1
                    else:
                        self.boardValues[0][temp] = -1
                else:
                    rowIndex = temp/15
                    colIndex = temp%15
                    if self.boardValues[rowIndex][colIndex] == -1:
                        x = x-1
                    else:
                        self.boardValues[rowIndex][colIndex] = -1
            #Calculating surrounding mine values (non-boundary)
            for i in range(1,self.rows-1):
                for j in range(1,self.columns-1):
                    counter = 0
                    if self.boardValues[i-1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j+1] == -1:
                        counter = counter + 1

                    if self.boardValues[i][j] != -1:
                        self.boardValues[i][j] = counter

            #Calculating surrounding mine values (top boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[0][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[0][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i] == -1:
                    counter = counter + 1
                if self.boardValues[1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[0][i] != -1:
                    self.boardValues[0][i] = counter

            #Calculating surrounding mine values (left boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][1] == -1:
                    counter = counter + 1
                if self.boardValues[i][1] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][1] == -1:
                    counter = counter + 1

                if self.boardValues[i][0] != -1:
                    self.boardValues[i][0] = counter

            #Calculating surrounding mine values (right boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][self.columns-1] == -1:
                    counter = counter + 1
                if self.boardValues[i][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-1] == -1:
                    counter = counter + 1

                if self.boardValues[i][self.columns-1] != -1:
                    self.boardValues[i][self.columns-1] = counter

            #Calculating surrounding mine values (bottom boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[self.rows-2][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[self.rows-1][i] != -1:
                    self.boardValues[self.rows-1][i] = counter

            #Calculating the corner values
            counter = 0
            if self.boardValues[1][0] == -1:
                counter = counter + 1
            if self.boardValues[0][1] == -1:
                counter = counter + 1
            if self.boardValues[1][1] == -1:
                counter = counter + 1
            self.boardValues[0][0] = counter

            counter = 0
            if self.boardValues[0][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-1] == -1:
                counter = counter + 1
            self.boardValues[0][self.columns-1] = counter

            counter = 0
            if self.boardValues[self.rows-2][0] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][1] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][0] = counter

            counter = 0
            if self.boardValues[self.rows-2][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][self.columns-1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][self.columns-2] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][self.columns-1] = counter

        #------------------------Expert------------------------
        
        elif self.difficulty == 2:
            self.mines = 99
            #Populating the field with mines
            for x in range(self.mines):
                temp = random.randrange(0,460)
                if temp < 30:
                    if self.boardValues[0][temp] == -1:
                        x = x-1
                    else:
                        self.boardValues[0][temp] = -1
                else:
                    rowIndex = temp/29
                    colIndex = temp%29
                    if self.boardValues[rowIndex][colIndex] == -1:
                        x = x-1
                    else:
                        self.boardValues[rowIndex][colIndex] = -1
            #Calculating surrounding mine values (non-boundary)
            for i in range(1,self.rows-1):
                for j in range(1,self.columns-1):
                    counter = 0
                    if self.boardValues[i-1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i-1][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i][j+1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j-1] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j] == -1:
                        counter = counter + 1
                    if self.boardValues[i+1][j+1] == -1:
                        counter = counter + 1

                    if self.boardValues[i][j] != -1:
                        self.boardValues[i][j] = counter

            #Calculating surrounding mine values (top boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[0][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[0][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[1][i] == -1:
                    counter = counter + 1
                if self.boardValues[1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[0][i] != -1:
                    self.boardValues[0][i] = counter

            #Calculating surrounding mine values (left boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][1] == -1:
                    counter = counter + 1
                if self.boardValues[i][1] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][0] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][1] == -1:
                    counter = counter + 1

                if self.boardValues[i][0] != -1:
                    self.boardValues[i][0] = counter

            #Calculating surrounding mine values (right boundary)
            for i in range(1,self.rows-1):
                counter = 0
                if self.boardValues[i-1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i-1][self.columns-1] == -1:
                    counter = counter + 1
                if self.boardValues[i][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-2] == -1:
                    counter = counter + 1
                if self.boardValues[i+1][self.columns-1] == -1:
                    counter = counter + 1

                if self.boardValues[i][self.columns-1] != -1:
                    self.boardValues[i][self.columns-1] = counter

            #Calculating surrounding mine values (bottom boundary)
            for i in range(1,self.columns-1):
                counter = 0
                if self.boardValues[self.rows-2][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-2][i+1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i-1] == -1:
                    counter = counter + 1
                if self.boardValues[self.rows-1][i+1] == -1:
                    counter = counter + 1

                if self.boardValues[self.rows-1][i] != -1:
                    self.boardValues[self.rows-1][i] = counter

            #Calculating the corner values
            counter = 0
            if self.boardValues[1][0] == -1:
                counter = counter + 1
            if self.boardValues[0][1] == -1:
                counter = counter + 1
            if self.boardValues[1][1] == -1:
                counter = counter + 1
            self.boardValues[0][0] = counter

            counter = 0
            if self.boardValues[0][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[1][self.columns-1] == -1:
                counter = counter + 1
            self.boardValues[0][self.columns-1] = counter

            counter = 0
            if self.boardValues[self.rows-2][0] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][1] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][0] = counter

            counter = 0
            if self.boardValues[self.rows-2][self.columns-2] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-2][self.columns-1] == -1:
                counter = counter + 1
            if self.boardValues[self.rows-1][self.columns-2] == -1:
                counter = counter + 1
            self.boardValues[self.rows-1][self.columns-1] = counter
            

#---------------------------------------------------------------------

#---------------------------------------------------------------------

    def clickBoard(self, row, column):
        #Location clicked is a bomb
        if self.boardValues[row][column] == -1:
            print "Boom! Game Over."
            #---------------Another action needed here?

        #Location clicked is a number other than 0
        elif self.boardValues[row][column] != 0:
            self.isRevealed[row][column] = True

        #Location clicked is a 0
        else:
            #MineBoard.reveal(self,row,column)
            self.isRevealed[row][column] = True
            for i in range(30):
                MineBoard.revealTouchingZeros(self)

#----------------------------------------------------------------------


    def revealTouchingZeros(self):
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):
                if self.boardValues[i-1][j-1] == 0 and self.isRevealed[i-1][j-1] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i-1][j] == 0 and self.isRevealed[i-1][j] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i-1][j+1] == 0 and self.isRevealed[i-1][j+1] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i][j-1] == 0 and self.isRevealed[i][j-1] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i][j+1] == 0 and self.isRevealed[i][j+1] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i+1][j-1] == 0 and self.isRevealed[i+1][j-1] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i+1][j] == 0 and self.isRevealed[i+1][j] == True:
                    self.isRevealed[i][j] = True
                if self.boardValues[i+1][j+1] == 0 and self.isRevealed[i+1][j+1] == True:
                    self.isRevealed[i][j] = True

        for i in range(self.columns-1):
            if self.boardValues[0][i-1] == 0 and self.isRevealed[0][i-1] == True:
                self.isRevealed[0][i] = True
            if self.boardValues[0][i+1] == 0 and self.isRevealed[0][i+1] == True:
                self.isRevealed[0][i] = True
            if self.boardValues[1][i-1] == 0 and self.isRevealed[1][i-1] == True:
                self.isRevealed[0][i] = True
            if self.boardValues[1][i] == 0 and self.isRevealed[1][i] == True:
                self.isRevealed[0][i] = True
            if self.boardValues[1][i+1] == 0 and self.isRevealed[1][i+1] == True:
                self.isRevealed[0][i] = True

            if self.boardValues[self.rows-2][i-1] == 0 and self.isRevealed[self.rows-2][i-1] == True:
                self.isRevealed[self.rows-1][i] = True
            if self.boardValues[self.rows-2][i] == 0 and self.isRevealed[self.rows-2][i] == True:
                self.isRevealed[self.rows-1][i] = True
            if self.boardValues[self.rows-2][i+1] == 0 and self.isRevealed[self.rows-2][i+1] == True:
                self.isRevealed[self.rows-1][i] = True
            if self.boardValues[self.rows-1][i-1] == 0 and self.isRevealed[self.rows-1][i-1] == True:
                self.isRevealed[self.rows-1][i] = True
            if self.boardValues[self.rows-1][i+1] == 0 and self.isRevealed[self.rows-1][i+1] == True:
                self.isRevealed[self.rows-1][i] = True

        for i in range(self.rows-1):
            if self.boardValues[i-1][0] == 0 and self.isRevealed[i-1][0] == True:
                self.isRevealed[i][0] = True
            if self.boardValues[i-1][1] == 0 and self.isRevealed[i-1][1] == True:
                self.isRevealed[i][0] = True
            if self.boardValues[i][1] == 0 and self.isRevealed[i][1] == True:
                self.isRevealed[i][0] = True
            if self.boardValues[i+1][0] == 0 and self.isRevealed[i+1][0] == True:
                self.isRevealed[i][0] = True
            if self.boardValues[i+1][1] == 0 and self.isRevealed[i-1][1] == True:
                self.isRevealed[i][0] = True

            if self.boardValues[i-1][self.columns-2] == 0 and self.isRevealed[i-1][self.columns-2] == True:
                self.isRevealed[i][self.columns-1] = True
            if self.boardValues[i-1][self.columns-1] == 0 and self.isRevealed[i-1][self.columns-1] == True:
                self.isRevealed[i][self.columns-1] = True
            if self.boardValues[i][self.columns-2] == 0 and self.isRevealed[i][self.columns-2] == True:
                self.isRevealed[i][self.columns-1] = True
            if self.boardValues[i+1][self.columns-2] == 0 and self.isRevealed[i+1][self.columns-2] == True:
                self.isRevealed[i][self.columns-1] = True
            if self.boardValues[i+1][self.columns-1] == 0 and self.isRevealed[i+1][self.columns-1] == True:
                self.isRevealed[i][self.columns-1] = True
        

    def printIsRevealed(self):
        for x in range(self.rows):
            print self.isRevealed[x]


        
