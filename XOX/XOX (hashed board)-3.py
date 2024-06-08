# Game - XOX
# ver: 3

import os
import sys
from msvcrt import getch
import random
import numpy as np
scrclr = lambda: os.system('cls')

# Load random bitstrings
rndBitS = np.load('BitStrings.npy')
# Function that hashes board states
def HashState(scr):
    h = 0
    for i in range(3):
        for j in range(3):
            if scr[i][j] != 0:
                h = h ^ rndBitS[3*i+j][scr[i][j]-1]
    return h

class XOXGame():
    
    board = [[0 for i in range(3)] for j in range(3)]   # Current playing board
    player = 1      #Current player

    # Reseting game if needed
    def __init__(self): 
        self.board = [[0 for i in range(3)] for j in range(3)]
        self.player = 1

    # Checkin if wanted move is available
    def checkMove(self, x, y):
        if self.board[x][y] == 0:
            return 1
        return 0

    # Submitting move
    def makeMove(self, x, y):
        self.board[x][y] = self.player
        self.player = self.player % 2 + 1

    # Checking if game ended
    # Return game winner (1 or 2), 3 for draw and 0 for other
    def isEnded(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and self.board[i][0] != 0:
                return self.board[i][0] # Winner
            
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and self.board[0][i] != 0:
                return self.board[0][i] # Winner

        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[1][1] != 0: return self.board[1][1] # Winner
        if self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[1][1] != 0: return self.board[1][1] # Winner
        for row in self.board:
            if 0 in row: return 0 # Stil playing
        return 3 # Draw

    # Return board state
    def getBoard(self): return self.board

    # Return curent player
    def getPlayer(self): return self.player

# Print current game state on screen
def printScr(game):
    scrclr()
    board = game.getBoard()
    sys.stdout.write('|'),
    for i in range(5): sys.stdout.write('-')
    print '|'
    for row in board:
        for cell in row:
            if cell == 0:  sys.stdout.write('| ')
            elif cell == 1: sys.stdout.write('|X')
            else: sys.stdout.write('|O')
        print '|'
        sys.stdout.write('|')
        for i in range(5): sys.stdout.write('-')
        print '|'

# Converting letters to indexes
def genX(c):
    if c in ['q', 'w', 'e']: return 0
    elif c in ['a', 's', 'd']: return 1
    else: return 2
def genY(c):
    if c in ['q', 'a', 'z']: return 0
    elif c in ['w', 's', 'x']: return 1
    else: return 2

def gpi(game): # Get Player Input
    inp = 'r'
    while not inp in ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']:
        inp = getch()
    moveSucc = game.checkMove(genX(inp), genY(inp))
    while not moveSucc:
        inp = getch()
        while not inp in ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']:
            inp = getch()
        moveSucc = game.checkMove(genX(inp), genY(inp))
    return (genX(inp), genY(inp))

# Deffinition of learning algorithm
class QLearner:

    # Reseting AI's parametres
    def __init__(self, vdict, g, att):
        self.vDict = vdict
        self.petnica = []
        self.gamma = g
        self.preA = -1
        self.actionToTest = att

    # Generate AI's move based on current board state and training data
    def makeMove(self, scr, repLast, used):
        # Hashing board state
        boardHash = HashState(scr)
        index = 0
        if not boardHash in self.vDict.keys():
            self.actionToTest[boardHash] = []
            self.actionToTest[boardHash].append(0)
            self.vDict[boardHash] = []
            self.vDict[boardHash].append([scr, [1024 for i in range(9)]])
        for i in range(len(self.vDict[boardHash])):
            if scr == self.vDict[boardHash][index][0]:
                index = i

        # Making array of available actions
        actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for u in used:
            actions.remove(u)
        # Chosing the way action will be selected
        if self.gamma == 2:
            # Chosing actions starting with first one to the last one
            if not boardHash in self.vDict.keys():
                self.actionToTest[boardHash][index] = 0
                self.vDict[boardHash][index] = [scr, [1024 for i in range(9)]]
            while not (self.actionToTest[boardHash][index] in actions):
                self.actionToTest[boardHash][index] = self.actionToTest[boardHash][index] + 1
                if self.actionToTest[boardHash][index] == 9: self.actionToTest[boardHash][index] = 0
            self.preA = self.actionToTest[boardHash][index]
            self.actionToTest[boardHash][index] = self.actionToTest[boardHash][index] + 1
            if self.actionToTest[boardHash][index] == 9: self.actionToTest[boardHash][index] = 0
        elif self.gamma == 1:
            # Chosing action with hiest value form all available actions - can only be used with imported vDict, not in training
            self.preA = actions[0]
            for i in range(1,9):
                if i in actions:
                    if self.vDict[boardHash][index][1][i] > self.vDict[boardHash][index][1][self.preA]:
                        self.preA = i
        elif random.random() < self.gamma:
            # Chosing action by using weighted random
            su = 0
            usu = 0
            for a in actions: usu = usu + self.vDict[boardHash][index][a]
            rnd = random.randint(0, int(usu))
            for a in actions:
                su = su + self.vDict[boardHash][index][a]
                if rnd <= su:
                    self.preA = a
                    break
        else:
            # Choisng action by random pick from available actions
            self.preA = random.choice(actions)
        self.petnica.append([boardHash, index, self.preA])
        return self.preA

    # Evaluating learners reward
    def giveRew(self, status):
        if status == 0: return
        # Going back thrue state-action list
        for s in list(reversed(self.petnica)):
            if status > 0:
                # For positive reward
                for i in range(9):
                    if i == s[2]:
                        self.vDict[s[0]][s[1]][1][i] = (1-(status/64))*self.vDict[s[0]][s[1]][1][i] + 144*status
                    else:
                        self.vDict[s[0]][s[1]][1][i] = self.vDict[s[0]][s[1]][1][i]*(1-(status/64))
            else:
                # For negative reward
                for i in range(9):
                    if i != s[2]:
                        self.vDict[s[0]][s[1]][1][i] = self.vDict[s[0]][s[1]][1][i]*(1+(-status*self.vDict[s[0]][s[1]][1][s[2]])/(64*(9*1024-self.vDict[s[0]][s[1]][1][s[2]])))
                self.vDict[s[0]][s[1]][1][s[2]] = self.vDict[s[0]][s[1]][1][s[2]]*(1-(-status/64))
            # Decreasing status before rewarding next state (previous)
            status = status / 2
            if status == 1: break

# Get computer input
def gci(game, learner):
    usedMoves = []
    for i in range(3):
        for j in range(3):
            if game.getBoard()[i][j] != 0: 
                usedMoves.append(i*3+j)
    a = learner.makeMove(game.getBoard(), False, usedMoves)
    x = int(a/3)
    y = a % 3
    return (x, y)

# Get random input
def gri(game):
    a = random.randint(0, 8)
    x = int(a/3)
    y = a % 3
    moveSucc = game.checkMove(x, y)
    while not moveSucc:
        a = random.randint(0, 8)
        x = int(a/3)
        y = a % 3
        moveSucc = game.checkMove(x, y)
    return (x, y)


# Etimated rewards other then those on the end of the game
rews = {'win': 16.0, 'lose': -16.0, 'draw': 0.0, 'winpos': 0.0, 'block': 0.0}
# Recognition of those rewards
def getRew(board, x, y):
    pl = board[x][y]
    rew = 0.0

    # Columns check
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[x][i] == pl: plco = plco + 1
        elif board[x][i] == 0: emco = emco + 1
        else: opco = opco + 1
    if plco == 2 and emco == 1: rew = rews['winpos']
    if plco == 1 and opco == 2: return rews['block']
        
    # Rows check
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[i][y] == pl: plco = plco + 1
        elif board[i][y] == 0: emco = emco + 1
        else: opco = opco + 1
        if plco == 2 and emco == 1: rew = rews['winpos']
        if plco == 1 and opco == 2: return rews['block']

    # Diagonals check
    if (x, y) in [(0,0), (1,1), (2,2)]:
        plco = 0
        emco = 0
        opco = 0
        for i in range(3):
            if board[i][i] == pl: plco = plco + 1
            elif board[i][i] == 0: emco = emco + 1
            else: opco = opco + 1
        if plco == 2 and emco == 1: rew = rews['winpos']
        if plco == 1 and opco == 2: return rews['block']
    if (x, y) in [(0,2), (1,1), (2,0)]:
        plco = 0
        emco = 0
        opco = 0
        for i in range(3):
            if board[i][2-i] == pl: plco = plco + 1
            elif board[i][2-i] == 0: emco = emco + 1
            else: opco = opco + 1
        if plco == 2 and emco == 1: rew = rews['winpos']
        if plco == 1 and opco == 2: return rews['block']
        
    return rew

# Initialisation of game variables
"""
 mode:
 1 - multiplayer
 2 - single player X - player
 3 - sigle player X - PC
 4 - AI vs AI
 5 - AI vs random X - AI
 6 - AI vs random X - rnd
"""
mode = 6

state = 0 # Stil playing
draws = 0
wins = 0
loss = 0
iters = 100000
"""For best oponent set True, for training False"""
UseRandom = False
vDict = {}
aTT1 = {}
aTT2 = {}

# Loading generated training data if it exists
if os.path.exists('trainingFile.npy'):
    loadList = np.load('trainingFile.npy').tolist()
    vDict.clear()
    for inst in loadList:
        vDict[inst[1]] = inst[0]
        aTT1[inst[1]] = []
        aTT2[inst[1]] = []
        for h in inst:
            aTT1[inst[1]].append(0)
            aTT2[inst[1]].append(0)
            
    print 'vDict loaded.'

for its in range (iters):

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
    qLearner1 = QLearner(vDict, gamma, aTT1)
    qLearner2 = QLearner(vDict, gamma, aTT2)

    # Printin screen for game modes for 1 or 2 players
    if mode < 4:
        printScr(game)

    # Begining of one game from 
    state = 0 # Stil playing
    while state == 0:
        move = (-1, -1)
        pl = game.getPlayer()
        
        if mode == 1:       # Multiplayer mode
            move = gpi(game)
        elif mode == 2:     # Single player mode - CP plays O
            if pl == 1:
                move = gpi(game)
            else: move = gci(game, qLearner1)
        elif mode == 3:     # Single player mode - CP plays X
            if pl == 1:
                move = gci(game, qLearner1)
            else: move = gpi(game)
        elif mode == 4:     # AI vs AI mode (majority of draws expected)
            if pl == 1:
                move = gci(game, qLearner1)
            else:
                move = gci(game, qLearner2)
        elif mode == 5:     # AI vs random mode (AI plays X)
            if pl == 1:
                move = gci(game, qLearner1)
            else:
                move = gri(game)
        elif mode == 6:     # AI vs random mode (AI plays O)
            if pl == 1:
                move = gri(game)
            else:
                move = gci(game, qLearner1)
        
        game.makeMove(move[0], move[1])
        if mode < 4:        # Printing debuging information
            printScr(game)
            num = ""
            scr1 = np.array(game.getBoard()).ravel()
            for x in scr1: num = num + str(x)
            num1 = int(num, 3)
            #print vDict[num1], sum(vDict[num1]) # print vMat[num1], sum(vMat[num1])
        state = game.isEnded()
        rew = getRew(game.getBoard(), move[0], move[1]) # Calculating non-termilal rewards
        #if state == 1: print 'X wins!'
        #elif state == 2: print 'O wins!'
        #elif state == 3: print 'Draw!'
        # Assignment of rewards
        if mode == 2:
            if state == 2: qLearner1.giveRew(rews['win'])
            elif state == 1: qLearner1.giveRew(rews['lose'])
            elif state == 3: qLearner1.giveRew(rews['draw'])
            else: qLearner1.giveRew(rew)
        elif mode == 3:
            if state == 1: qLearner1.giveRew(rews['win'])
            elif state == 2: qLearner1.giveRew(rews['lose'])
            elif state == 3: qLearner1.giveRew(rews['draw'])
            else: qLearner1.giveRew(rew)
        elif mode == 4:
            if state == 1:
                qLearner1.giveRew(rews['win'])
                qLearner2.giveRew(rews['lose'])
                wins = wins + 1
            elif state == 2:
                qLearner1.giveRew(rews['lose'])
                qLearner2.giveRew(rews['win'])
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(rews['draw'])
                qLearner2.giveRew(rews['draw'])
                draws = draws + 1
            else:
                if game.getPlayer() == 1:
                    qLearner1.giveRew(rew)
                else:
                    qLearner2.giveRew(rew)
        elif mode == 5:
            if state == 1:
                qLearner1.giveRew(rews['win'])
                wins = wins + 1
            elif state == 2:
                qLearner1.giveRew(rews['lose'])
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(rews['draw'])
                draws = draws + 1
            else: qLearner1.giveRew(rew)
        elif mode == 6:
            if state == 2:
                qLearner1.giveRew(rews['win'])
                wins = wins + 1
                
            elif state == 1:
                qLearner1.giveRew(rews['lose'])
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(rews['draw'])
                draws = draws + 1
            else: qLearner1.giveRew(rew)

print wins, loss, draws

# Saving trainig data to file
if UseRandom:
    saveList = [(v, k) for k, v in vDict.iteritems()]
    np.save('trainingFile', saveList)
