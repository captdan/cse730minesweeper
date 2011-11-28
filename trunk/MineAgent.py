import sqlite3
from Action import Action

class MineAgent:
        #initializes agent with attributes and connection to existing
        #database
        def __init__(self, name, scope, learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward, revealedReward, unrevealedReward, connection):
            #set attributes from arguments
            self.name = name
            self.scope = scope
            self.learningCoefficient = learningCoefficient
            self.mineReward = mineReward
            self.correctFlagReward = correctFlagReward
            self.incorrectFlagReward = incorrectFlagReward
            self.unknownFlagReward = unknownFlagReward
            self.revealedReward = revealedReward
            self.unrevealedReward = unrevealedReward
            self.conn = connection
        
        @classmethod
        def getConnection(cls, name):
            conn = sqlite3.connect('db/' + name)
            conn.row_factory = sqlite3.Row
            return conn

        @classmethod
        def create(cls, name, scope, learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward,
                unknownFlagReward, revealedReward, unrevealedReward):
            #create new database schema
            conn = cls.getConnection(name)
            f = open('create_schema.sql', 'r')
            sql = f.read()
            f.close()
            conn.executescript(sql)
            #populate constants table
            conn.execute('''insert into constants values ({}, {}, {}, {}, {}, {}, {}, {})'''.format(learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward, revealedReward, unrevealedReward, scope))
            conn.commit()
            return cls(name, scope, learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward,
                revealedReward, unrevealedReward, conn)
        @classmethod
        def load(cls, name):
            #load existing database schema
            conn = cls.getConnection(name)
            cur = conn.cursor()
            cur.execute("select * from constants")
            r = cur.fetchone()
            learningCoefficient = r['learningCoefficient']
            mineReward = r['mineReward']
            correctFlagReward = r['correctFlagReward']
            incorrectFlagReward = r['incorrectFlagReward']
            unknownFlagReward = r['unknownFlagReward']
            revealedReward = r['revealedReward']
            unrevealedReward = r['unrevealedReward']
            scope = r['scope']
            return cls(name, scope, learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward,
                revealedReward, unrevealedReward, conn)


        #getters and setters for attributes (other than scope)
        def saveConstant(self, name, value):
            self.conn.execute('update constants set {} = {}'.format(name, value))

        def centerTile(self, queryString):
           index = (len(queryString) - 1) / 2
           return queryString[index]

        def replaceCenterTile(self, queryString, replacement):
            center = (len(queryString) - 1) / 2
            return queryString[0:center] + replacement + queryString[center:]

        #play a game of minesweeper
        def play(self, board):
            gameLog = []
            contin = True
            while(contin):
                #look through board for optimal move
                plannedAction = None
                for x in range(board.rows):
                    for y in range(board.columns):
                        q = board.query(x, y, self.scope)
                        center = self.centerTile(q)
                        cur = self.conn.cursor()
                        #if the center tile is unrevealed
                        if center == 'X' or center == 'F':
                            #evaluate reveal action
                            u = self.expectedRevealUtility(q)
                            #TODO: write this to a log file instead of stdout
                            print 'reveal (' + str(x) + ',' + str(y) + '):' + str(u) + '(' + q + ')' + center
                            if plannedAction == None or u > plannedAction.expectedUtility:
                                plannedAction = Action(Action.REVEAL, u, q, x, y)
                            #prepare current utility for upcoming checks
                            currentUtility = self.stateUtility(q)
                        #if the center tile is unrevealed and unflagged
                        if center == 'X':
                            #evaluate flag action
                            nextState = self.replaceCenterTile(q, 'F')
                            u = self.stateUtility(nextState) - currentUtility
                            if u > plannedAction.expectedUtility:
                                plannedAction = Action(Action.FLAG, u, q, x, y)
                        elif center == 'F':
                            #evaluate unflag action
                            nextState = self.replaceCenterTile(q, 'X')
                            u = self.stateUtility(nextState) - currentUtility
                            if u > plannedAction.expectedUtility:
                                plannedAction = Action(Action.UNFLAG, u, q, x, y)
                #execute and log planned action
                plannedAction.execute(board)
                gameLog.append(plannedAction)
                contin = (not board.win()) and (not board.loss())
                print board.prettyPrint()
            #save reveal history and update utility
            for x in gameLog:
                pass




        #if the given state is defined in the database, return its utility
        #otherwise, create the state in the database with utility equal to its reward                    
        def stateUtility(self, state):
            cur = self.conn.cursor()
            cur.execute("select utility from states where identity = '{}'".format(state))
            r = cur.fetchone()
            if r == None:
                center = self.centerTile(state)
                if center == 'X':
                    reward = self.unrevealedReward
                elif center == 'F':
                    reward = self.unknownFlagReward
                elif center == 'M':
                    reward = self.mineReward
                else:
                    reward = self.revealedReward
                cur.execute("insert into states values('{}','{}')".format(state, reward)) 
                cur.close()
                return reward
            else:
                util = r[0]
                cur.close()
                return util
            

        def expectedRevealUtility(self, state):
            cur = self.conn.cursor()
            currentStateUtility = self.stateUtility(state)
            #either fix sql to do this, or just compute it in python
            cur.execute("select sum(occurances * utility) / sum(occurances) from reveal_transitions join states on identity = destination where start = '{}'".format(state))
            r = cur.fetchone()
            if r[0] == None:
                #no history
                #assume no mine will be revealed
                util = self.revealedReward - currentStateUtility
            else:
                util = r[0] - currentStateUtility
            cur.close() 
            return util



