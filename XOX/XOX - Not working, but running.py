import os
import sys
from msvcrt import getch
import random
import numpy as np
scrclr = lambda: os.system('cls')

class XOXGame():
    
    board = [[0 for i in range(3)] for j in range(3)]
    player = 1
        
    def __init__(self):
        self.board = [[0 for i in range(3)] for j in range(3)]
        self.player = 1

    def checkMove(self, x, y):
        if self.board[x][y] == 0:
            return 1
        return 0

    def makeMove(self, x, y):
        self.board[x][y] = self.player
        self.player = self.player % 2 + 1

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

    def getBoard(self): return self.board

    def getPlayer(self): return self.player

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

class QLearner:

    def __init__(self, vmat, g):
        self.vMat = vmat
        self.petnica = []
        self.gamma = g
        self.preA = -1

    def makeMove(self, scr, repLast, used):
        num = ""
        scr1 = np.array(scr).ravel()
        for x in scr1: num = num + str(x)
        num1 = int(num, 3)
        #if self.preA > -1 and not repLast:
        #if self.preA != -1: self.petnica.append([num1, self.preA])         prebaceno dole, mozda treba da se vrati!
        #print self.petnica
        #getch()

        actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for u in used:
            actions.remove(u)
        if random.random() < self.gamma:
            su = 0
            rnd = random.randint(0, su)
            for i in range(len(actions)):
                su = su + actions[i]
                if rnd <= su:
                    self.preA = actions[i]
                    break
                #for j in range(self.vMat[num1][i]+1-min(self.vMat[num1])):
                #    actions.append(i)
        else: self.preA = random.choice(actions)
        if self.preA != -1: self.petnica.append([num1, self.preA])
        else: print 'asd'
        return self.preA
            
        """if random.random() < self.gamma and not repLast:
            pom = max(self.vMat[num1])
            self.preA = [i for i, j in enumerate(self.vMat[num1]) if j == pom][0]
            return self.preA
        self.preA = random.randint(0,8)
        return self.preA"""

    def giveRew(self, status):
        if status == 0: return
        rew = status*4
        #print list(reversed(self.petnica)), self.petnica, status
        for s in list(reversed(self.petnica)):
            if rew > 0:
                if rew - 2 <= 0: break
                rew = rew - 2
            else:
                if rew + 2 >= 0: break
                rew = rew + 2
            self.vMat[s[0]][s[1]] = self.vMat[s[0]][s[1]] + rew
        #for f in self.vMat:
        #    if sum(f) != 9: print f
        #print
        #getch()

def gci(game, learner): # Get Computer Input
    usedMoves = []
    for i in range(3):
        for j in range(3):
            if game.getBoard()[i][j] != 0: 
                usedMoves.append(i*3+j)
    a = learner.makeMove(game.getBoard(), False, usedMoves)
    x = int(a/3)
    y = a % 3
    moveSucc = game.checkMove(x, y)
    return (x, y)

def gri(game): # Get Random Input
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

def getRew(board, x, y):
    pl = board[x][y]
    rew = 1
    
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[x][i] == pl: plco = plco + 1
        elif board[x][i] == 0: emco = emco + 1
        else: opco = opco + 1
    if plco == 2 and emco == 1: rew = 3
    if plco == 1 and opco == 2: rew = 8
        
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[i][y] == pl: plco = plco + 1
        elif board[i][y] == 0: emco = emco + 1
        else: opco = opco + 1
    if plco == 2 and emco == 1: rew = 3
    if plco == 1 and opco == 2: rew = 8
                    
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[i][i] == pl: plco = plco + 1
        elif board[i][i] == 0: emco = emco + 1
        else: opco = opco + 1
    if plco == 2 and emco == 1: rew = 3
    if plco == 1 and opco == 2: rew = 8
    
    plco = 0
    emco = 0
    opco = 0
    for i in range(3):
        if board[i][2-i] == pl: plco = plco + 1
        elif board[i][2-i] == 0: emco = emco + 1
        else: opco = opco + 1
    if plco == 2 and emco == 1: rew = 3
    if plco == 1 and opco == 2: rew = 8
    
    return rew

# Initialisation
"""
 mode:
 1 - multiplayer
 2 - single player X - player
 3 - sigle player X - PC
 4 - AI vs AI
 5 - AI vs random X - AI
 6 - AI vs random X - rnd
"""
mode = 4

state = 0 # Stil playing
draws = 0
wins = 0
loss = 0
iters = 100000
dontUseRandom = False
vMat = [[1 for i in range(9)] for j in range(20000)]
if os.path.exists('trainingFile.npy') and not dontUseRandom: vMat = np.load('trainingFile.npy').tolist()

for its in range (iters):

    if its % 1000 == 0: print its, state
    if its == iters-10:
        mode = 3
        td = 0
        tu = 0
        for x in vMat:
            for y in x:
                if y < td:
                    td = y
                if y > tu:
                    tu = y
            
        print td, tu
        print wins, loss, draws
        getch()

    game = XOXGame()
    """gamma = 0.1
    if its > iters/2: gamma = 0.3
    if its > iters/5*3: gamma = 0.5
    if its > iters/5*4: gamma = 0.7"""
    gamma = 0.75/iters*its+0.1
    if dontUseRandom: gamma = 1
    qLearner1 = QLearner(vMat, 0.75/iters*its+0.1)
    qLearner2 = QLearner(vMat, 0.75/iters*its+0.1)
    if mode < 4:
        printScr(game)
    state = 0 # Stil playing
    while state == 0:
        move = (-1, -1)
        pl = game.getPlayer()
        
        if mode == 1:
            move = gpi(game)
        elif mode == 2:
            if pl == 1:
                move = gpi(game)
            else: move = gci(game, qLearner1)
        elif mode == 3:
            if pl == 1:
                move = gci(game, qLearner1)
            else: move = gpi(game)
        elif mode == 4:
            if pl == 1:
                move = gci(game, qLearner1)
            else:
                move = gci(game, qLearner2)
        elif mode == 5:
            if pl == 1:
                move = gci(game, qLearner1)
            else:
                move = gri(game)
        elif mode == 6:
            if pl == 1:
                move = gri(game)
            else:
                move = gci(game, qLearner1)
        
        game.makeMove(move[0], move[1])
        if mode < 4:
            printScr(game)
            #for g in range(len(vMat)):
            #    if sum(vMat[g]) != 9: print g, vMat[g]
            #print 
        state = game.isEnded()
        rew = getRew(game.getBoard(), move[0], move[1])
        #if state == 1: print 'X wins!'
        #elif state == 2: print 'O wins!'
        #elif state == 3: print 'Draw!'
        if mode == 2:
            if state == 2: qLearner1.giveRew(10)
            elif state == 1: qLearner1.giveRew(-20)
            elif state == 3: qLearner1.giveRew(3)
            else: qLearner1.giveRew(rew)
        elif mode == 3:
            if state == 1: qLearner1.giveRew(10)
            elif state == 2: qLearner1.giveRew(-20)
            elif state == 3: qLearner1.giveRew(3)
            else: qLearner1.giveRew(rew)
        elif mode == 4:
            if state == 1:
                qLearner1.giveRew(10)
                qLearner2.giveRew(-20)
                wins = wins + 1
                qLearner1.giveRew(-20)
                qLearner2.giveRew(10)
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(3)
                qLearner2.giveRew(3)
                draws = draws + 1
            else: qLearner1.giveRew(rew)
        elif mode == 5:
            if state == 1:
                qLearner1.giveRew(10)
                wins = wins + 1
            elif state == 2:
                qLearner1.giveRew(-20)
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(3)
                draws = draws + 1
            else: qLearner1.giveRew(rew)
        elif mode == 5:
            if state == 2:
                qLearner1.giveRew(10)
                wins = wins + 1
            elif state == 1:
                qLearner1.giveRew(-20)
                loss = loss + 1
            elif state == 3:
                qLearner1.giveRew(3)
                draws = draws + 1
            else: qLearner1.giveRew(rew)
td = 0
tu = 0
for x in vMat:
    for y in x:
        if y < td:
            td = y
        if y > tu:
            tu = y
    
print td, tu
print wins, loss, draws

if not dontUseRandom: np.save('trainingFile', vMat)
