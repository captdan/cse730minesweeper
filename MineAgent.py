import sqlite3

class MineAgent:
        #Initializes agent from name only;
        #requires existing agent with given name
	def __init__(self, name):
            #set name = name, and load qualities of agent from
            #sqlite database
            self.name = name
            self.conn = sqlite3.connect('db/' + name)
            self.conn.row_factory = sqlite3.Row
            self.load()
        def __init__(self, name, scope, learningCoefficient, mineReward, correctFlagReward, incorrectFlagReward, unknownFlagReward, revealedReward, unrevealedReward):
            #set attributes from arguments and create sqlite database
            #there is probably a better way to do this
            self.name = name

            self.conn = sqlite3.connect('db/' + name)
            self.conn.row_factory = sqlite3.Row

            self.scope = scope
            self.learningCoefficient = learningCoefficient
            self.mineReward = mineReward
            self.correctFlagReward = correctFlagReward
            self.incorrectFlagReward = incorrectFlagReward
            self.unknownFlagReward = unknownFlagReward
            self.revealedReward = revealedReward
            self.unrevealedReward = unrevealedReward
            self.create()

        def create(self):
            #create new database schema
            f = open('create_schema.sql')
            sql = f.read()
            self.conn.executescript(sql)
            #populate constants table
            self.conn.execute('''insert into constants values ({}, {}, {}, {}, {}, {}, {}, {})'''.format(self.learningCoefficient, self.mineReward, self.correctFlagReward, self.incorrectFlagReward, self.unknownFlagReward, self.revealedReward, self.unrevealedReward, self.scope))
            self.conn.commit()

        def load(self):
            cur = self.conn.cursor()
            cur.execute("select * from constants")
            r = cur.fetchone()
            self.learningCoefficient = r['learningCoefficient']
            self.mineReward = r['mineReward']
            self.correctFlagReward = r['correctFlagReward']
            self.incorrectFlagReward = r['incorrectFlagReward']
            self.unknownFlagReward = r['unknownFlagReward']
            self.revealedReward = r['revealedReward']
            self.unrevealedReward = r['unrevealedReward']
            self.scope = r['scope']

        #getters and setters for attributes (other than scope)
        def saveConstant(self, name, value):
            self.conn.execute('update constants set {} = {}'.format(name, value)


            
