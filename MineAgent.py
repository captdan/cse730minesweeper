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
            conn.execute('''insert into constants values ({}, {}, {}, {}, {}, {}, {}, {});'''.format(learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward, revealedReward, unrevealedReward, scope))
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
            self.conn.execute('update constants set {} = {};'.format(name, value))

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
            flagLogged = set()
            for x in gameLog:
                if x.actionType == Action.REVEAL:
                    self.addTransition(x.startState, x.endState)
                    self.stateUtility(x.endState)
                    
                elif x.actionType == Action.FLAG:
                    if not x.endState in flagLogged:
                        self.addFlagHistory(x.endState, board.tiles[x.x][x.y].mine)
                        flagLogged.add(x.endState)
                        #update utility in database
                        self.updateFlagUtility(x.endState)


        #if the given state is defined in the database, return its utility
        #otherwise, create the state in the database with utility equal to its reward                    
        def stateUtility(self, state):
            cur = self.conn.cursor()
            cur.execute("select utility from states where identity = '{}';".format(state))
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
                cur.execute("insert into states values('{}','{}');".format(state, reward)) 
                self.conn.commit()
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
            cur.execute("select sum(occurances * utility) / sum(occurances) from reveal_transitions join states on identity = destination where start = '{}';".format(state))
            r = cur.fetchone()
            if r[0] == None:
                #no history
                #assume no mine will be revealed
                util = self.revealedReward - currentStateUtility
            else:
                util = r[0] - currentStateUtility
            cur.close() 
            return util


        def addTransition(self, start, end):
            cur = self.conn.cursor()
            cur.execute("select * from reveal_transitions where start = '{}' and destination = '{}';".format(start, end))
            r = cur.fetchone()
            if r == None:
                cur.execute("insert into reveal_transitions(start, destination, occurances) values ('{}','{}',1);".format(start, end))
                self.conn.commit()
            else:
                cur.execute("update reveal_transitions set occurances = occurances + 1 where start = '{}' and destination = '{}';".format(start, end))
                self.conn.commit()
            cur.close()

        def addFlagHistory(self, state, correct):
            cur = self.conn.cursor()
            cur.execute("select * from flag_history where identity = '{}';".format(state))
            r = cur.fetchone()
            if r == None:
                cur.execute("insert into flag_history values('{}', 0, 0);".format(state))
            if correct:
                cur.execute("update flag_history set correctFlags = correctFlags + 1 where identity = '{}';".format(state))
            else:
                cur.execute("update flag_history set incorrectFlags = incorrectFlags + 1 where identity = '{}';".format(state))
            self.conn.commit()


        def updateFlagUtility(self, state):
            cur = self.conn.cursor()
            cur.execute("select * from flag_history where identity = '{}';".format(state))
            r = cur.fetchone()
            incorrectFlags = r['incorrectFlags']
            correctFlags = r['correctFlags']
            util = self.unknownFlagReward + (correctFlags * self.correctFlagReward + incorrectFlags * self.incorrectFlagReward) / (correctFlags + incorrectFlags)
            cur.execute("update states set utility = {};".format(util))

            cur.close()
            self.conn.commit()
