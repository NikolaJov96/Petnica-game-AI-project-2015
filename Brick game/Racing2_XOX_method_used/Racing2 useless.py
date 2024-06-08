# game - Racing
# ver: 2

import QLearner

class RacingGame():

    board = [[0 for i in range(10)] for j in range(36)] # Current screen
    plPos = 1 # Side on which players car is
    score = 0 # Current game score
    sideIt = 0 # Counter used for printing deges of the road
    op = [-1, -1, -1] # Opnents positions (-1 - no oponents on screen)

    # Reseting game if needed
    def __init__(self):
        self.board = [[0 for i in range(10)] for j in range(36)]
        self.plPos = 1
        self.score = 0
        self.sideIt = 0
        self.op = [-1, -1, -1]

    # Checkin if wanted move is available
    def checkMove(self, d):
        # 1 - left; 2 - staty; 3 - right
        if plPos == 1 and d == 1: return False
        elif plPos == 2 and d == 3: return False
        return True

    # Submitting move
    def makeMove(self, d):
        self.board[x][y] = self.player
        self.player = self.player % 2 + 1
    
    # Checking if game ended
    def isEnded(self):
        return False

    # Print current game state on screen
    def printScr(self, scr):
        clear = lambda: os.system('cls')
            clear()
            print 'Your score is:', score
            for i in range(3, 23):
                for j in range(0,10):
                    if disp[i][j] == 0: print ' ',
                    else: print '#',
                print

# Initialisation of game variables
def startGame(mode):
    iters = 10
    vDict = {}
    aTT = {} # Action to test

    if os.path.exists('trainingFile.npy'):
        loadList = np.load('trainingFile.npy').tolist()
        vDict.clear()
        for inst in loadList:
            vDict[inst[1]] = inst[0]
            aTT[inst[1]] = []
            for h in inst:
                aTT[inst[1]].append(0)
                
        print 'vDict loaded.'

    for its in range(iters):
        
        # Printing current state of game counters
        if its % 1000 == 0: print its, state
        
        # Switching last couple of iterations to singleplayer for easier debug

        # Reinitialisation of game
        game = XOXGame()

        # Reinitialisation of gamma coef. which influences way of picing best actions
        """gamma = 0.1
        if its > iters/2: gamma = 0.3
        if its > iters/5*3: gamma = 0.5
        if its > iters/5*4: gamma = 0.7"""
        #gamma = 0.8/iters*its+0.1
        gamma = 2
        if not UseRandom: gamma = 1

        # Reinitialising learner objects (table with training tada is not reseted)
        qLearner = QLearner(vDict, gamma, aTT)

        # Printin screen for game modes for 1 or 2 players
        if mode < 2:
            printScr(game)

        crash = False
        while not crash:
            move = 2
            if mode == 1:
                while not inp in ['a', 's', 'd']:
                    inp = getch()
                move = ['a', 's', 'd'].index(inp)+1
            elif mode == 2:
                move = qLearner.makeMove()#HOW?

            game.makeMove(move)

            if mode < 3:
                printScr(game.getScrean)

            qLearner.giveRew()







