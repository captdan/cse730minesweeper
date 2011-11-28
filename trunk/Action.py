import math

class Action:
    REVEAL = 0
    FLAG = 1
    UNFLAG = 2
    def __init__(self, actionType, expectedUtility, startState, x, y):
        self.actionType = actionType
        self.expectedUtility = expectedUtility
        self.startState = startState
        self.x = x
        self.y = y
        self.scope = math.sqrt(len(startState))
    def execute(self, board):
        if self.actionType == Action.REVEAL:
            board.reveal(self.x,self.y)
        elif self.actionType == Action.FLAG:
            board.flag(self.x,self.y) 
        elif self.actionType == Action.UNFLAG:
            board.unflag(self.x,self.y)
        self.endState = board.query(self.x, self.y, self.scope)
    
