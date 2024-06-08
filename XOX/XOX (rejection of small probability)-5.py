# Game - XOX
# ver: 5

import os
import sys
from msvcrt import getch
import random
import numpy as np
import hashlib
scrclr = lambda: os.system('cls')

# Load random bitstrings
rndBitS = np.load('BitStrings.npy')
# Function that hashes board states
def HashState(scr):
    h = hashlib.md5()
    h.update(str(scr))
    return h.hexdigest()

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
        weigh = 0
        
        # Check if player can make move that wins or blocks win
        abledToWinn = False
        abledToBlock = False
        for i in range(3):
            pl = 0
            emp = 0
            op = 0
            for j in range(3):
                if self.board[i][j] == self.player: pl = pl + 1
                elif self.board[i][j] == 0: emp = emp + 1
                else: op = op + 1
            if pl == 2 and emp == 1:
                #print 'a1', pl, emp, op
                abledToWinn = True
            if op == 2 and emp == 1:
                #print 'a2', pl, emp, op
                abledToBlock = True
        for j in range(3):
            pl = 0
            emp = 0
            op = 0
            for i in range(3):
                if self.board[i][j] == self.player: pl = pl + 1
                elif self.board[i][j] == 0: emp = emp + 1
                else: op = op + 1
            if pl == 2 and emp == 1:
                #print 'a1', pl, emp, op
                abledToWinn = True
            if op == 2 and emp == 1:
                #print 'a2', pl, emp, op
                abledToBlock = True
        if not abledToWinn:
            pl = 0
            emp = 0
            op = 0
            for i in range(3):
                if self.board[i][i] == self.player: pl = pl + 1
                elif self.board[i][i] == 0: emp = emp + 1
                else: op = op + 1
            if pl == 2 and emp == 1: abledToWinn = True
            if op == 2 and emp == 1: abledToBlock = True
        if not abledToWinn:
            pl = 0
            emp = 0
            op = 0
            for i in range(3):
                if self.board[i][2-i] == self.player: pl = pl + 1
                if self.board[i][2-i] == 0: emp = emp + 1
                else: op = op + 1
            if pl == 2 and emp == 1: abledToWinn = True
            if op == 2 and emp == 1: abledToBlock = True
        # Setting new values
        self.board[x][y] = self.player

        # Check if move is made in some of the prmary positions
        # Columns check
        plco = 0
        emco = 0
        opco = 0
        for i in range(3):
            if self.board[x][i] == self.player: plco = plco + 1
            elif self.board[x][i] == 0: emco = emco + 1
            else: opco = opco + 1
        if plco == 3: weigh = 2.0 
        if plco == 1 and opco == 2:
            if not abledToWinn: weigh = 2.0
            else: weigh = 0.0
            
        # Rows check
        plco = 0
        emco = 0
        opco = 0
        for i in range(3):
            if self.board[i][y] == self.player: plco = plco + 1
            elif self.board[i][y] == 0: emco = emco + 1
            else: opco = opco + 1
        if plco == 3: weigh = 2.0
        if plco == 1 and opco == 2:
            if not abledToWinn: weigh = 2.0
            else: weigh = 0.0

        # Diagonals check
        if (x, y) in [(0,0), (1,1), (2,2)]:
            plco = 0
            emco = 0
            opco = 0
            for i in range(3):
                if self.board[i][i] == self.player: plco = plco + 1
                elif self.board[i][i] == 0: emco = emco + 1
                else: opco = opco + 1
            if plco == 3: weigh = 2.0
            if plco == 1 and opco == 2:
                if not abledToWinn: weigh = 2.0
                else: weigh = 0.0
        if (x, y) in [(0,2), (1,1), (2,0)]:
            plco = 0
            emco = 0
            opco = 0
            for i in range(3):
                if self.board[i][2-i] == self.player: plco = plco + 1
                elif self.board[i][2-i] == 0: emco = emco + 1
                else: opco = opco + 1
            if plco == 3: weigh = 2.0
            if plco == 1 and opco == 2:
                if not abledToWinn: weigh = 2.0
                else: weigh = 0.0

        if not (abledToBlock or abledToWinn):
            if x==1 and y==1: weigh = 2
            #else:
            #    if self.board[1][1] != 0:
            #        if (x,y) in [(0,2),(2,0),(0,0),(2,2)]:
            #            weigh = 2.0

            
        #print abledToWinn, abledToBlock, self.player, weigh
        #getch()
        self.player = self.player % 2 + 1
        return weigh

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
    def __init__(self, vdict):
        self.vDict = vdict
        self.petnica = []
        self.preA = -1

    # Generate AI's move based on current board state and training data
    def makeMove(self, scr, repLast, used):
        # Hashing board state
        boardHash = HashState(scr)
        if not boardHash in self.vDict.keys():
            self.vDict[boardHash] = [128.0 for i in range(9)]
            for i in used: self.vDict[boardHash][i] = 0

        # Making array of available actions
        actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for u in used:
            actions.remove(u)
        # Randmly picking availoble action that isnt labled with 0
        # Removing 0-graded actions
        for i in range(len(self.vDict[boardHash])):
            if (i in actions) and (self.vDict[boardHash][i] == 0):
                actions.remove(i)
        #if sum(self.vDict[boardHash]) > 9400:
        #    print self.vDict[boardHash], actions
        #    getch()
        if len(actions) == 0: print self.vDict[boardHash], actions, used
        self.preA = random.choice(actions)
        self.petnica.append([boardHash, self.preA])
        return self.preA

    # Evaluating learners reward
    def giveRew(self, status):
        if status == 0: return
        # Going back thrue state-action list
        for s in list(reversed(self.petnica)):
            if max(self.vDict[s[0]]) == 9*128:
                status = status / 2
                if status == 1: break
                continue
            posCo = 0
            for i in self.vDict[s[0]]: posCo = posCo + 1
            if status > 0:
                # For positive reward
                for i in range(9):
                    if self.vDict[s[0]][i] > 0:
                        self.vDict[s[0]][s[1]] = self.vDict[s[0]][s[1]] + 2
                        self.vDict[s[0]][i] = self.vDict[s[0]][i] - 2
            else:
                # For negative reward
                for i in range(9):
                    if self.vDict[s[0]][i] > 0:
                        self.vDict[s[0]][s[1]] = self.vDict[s[0]][s[1]] - 2
                        self.vDict[s[0]][i] = self.vDict[s[0]][i] + 2
                
            if sum(self.vDict[s[0]]) > 4700:
                print self.vDict[s[0]]
                getch()
            # Steting values colse to 0 to 0
            posCo = 0
            newZ = False
            for i in range(len(self.vDict[s[0]])):
                if self.vDict[s[0]][i] < 15:
                    if self.vDict[s[0]][i] != 0:
                        newZ = True
                        #print 'a',self.vDict[s[0]]
                    self.vDict[s[0]][i] = 0
                else: posCo = posCo + 1
            if newZ:
                for i in range(len(self.vDict[s[0]])):
                    if self.vDict[s[0]][i] != 0: self.vDict[s[0]][i] = 128.0
                #print self.vDict[s[0]]
                
            # Decreasing status before rewarding next state (previous)
            status = status / 2
            if status == 1: break
            #break

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
rews = {'win': 2.0, 'lose': -2.0, 'draw': 0.0, 'winpos': 0.0, 'block': 0.0}


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
iters = 400000
vDict = {}
aTT1 = {}
aTT2 = {}
winlos = []

# Loading generated training data if it exists
if os.path.exists('trainingFile.npy'):
    loadList = np.load('trainingFile.npy').tolist()
    vDict.clear()
    for inst in loadList:
        vDict[inst[1]] = inst[0]
            
    print 'vDict loaded.'

for its in range (iters):

    # Printing current state of game counters
    if its % 3000 == 0: print its, state
    if its % 10000 == 0:
        winlos.append([its, wins, loss, draws])
        wins = 0
        loss = 0
        draws = 0

    # Reinitialisation of game
    game = XOXGame()

    # Reinitialising learner objects (table with training tada is not reseted)
    qLearner1 = QLearner(vDict)
    qLearner2 = QLearner(vDict)

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
        
        rew = game.makeMove(move[0], move[1])
        if mode < 4:        # Printing debuging information
            printScr(game)
            #num = ""
            #scr1 = np.array(game.getBoard()).ravel()
            #for x in scr1: num = num + str(x)
            #num1 = int(num, 3)
            #print vDict[num1], sum(vDict[num1]) # print vMat[num1], sum(vMat[num1])
            #getch()
        state = game.isEnded()
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
            
print wins, loss, draws, len(vDict)
for rat in winlos: print rat


# Saving trainig data to file
saveList = [(v, k) for k, v in vDict.iteritems()]
np.save('trainingFile', saveList)
