# game - Racing
# var: 2

import os
import sys
from msvcrt import getch
import random
import numpy as np
import time
import copy
import hashlib
clear = lambda: os.system('cls')

# Load random bitstrings
rndBitS = np.load('BitStrings.npy')
# Function that hashes board states
def HashState(scr):
    #h = 0
    """for i in range(20):
        for j in range(10):
            if scr[i][j] != 0:
                h = h ^ rndBitS[3*i+j]"""

    
    h = hashlib.md5()
    h.update(str(scr))
    #print h.hexdigest()
    
    return h.hexdigest()

class RacingGame():
    disp = [[0 for i in range(10)] for j in range(36)]   # Current playing board
    score = 0
    it = -1
    sideit = 0
    plpos = 1
    op = [-1, -1, -1]
    for i in range(3, 23):
        if (i%3 == 0) or (i%3 == 1):
            disp[i][0] = 1
            disp[i][9] = 1
            
    # Reseting game if needed
    def __init__(self):
        self.disp = [[0 for i in range(10)] for j in range(36)]
        self.score = 0
        self.it = -1
        self.sideit = 0
        self.plpos = 1
        self.op = [-1, -1, -1]
        for i in range(3, 23):
            if (i%3 == 0) or (i%3 == 1):
                self.disp[i][0] = 1
                self.disp[i][9] = 1

    def printCar(self, x, y):     #printing each car
        self.disp[x][y]=1
        self.disp[x+1][y-1]=1
        self.disp[x+1][y]=1
        self.disp[x+1][y+1]=1
        self.disp[x+2][y]=1
        self.disp[x+3][y-1]=1
        self.disp[x+3][y]=1
        self.disp[x+3][y+1]=1

    def printCars(self, ite, c0, c1, c2, me):     #printing all cars
        if c0>-1: self.printCar(ite, c0*3)
        if c1>-1: self.printCar((ite+22)%33, c1*3)
        if c2>-1: self.printCar((ite+11)%33, c2*3)
        self.printCar(19, me*3)

    # Submitting move and calculating all movements
    def makeMove(self, move):
        if move == 1: self.plpos = 1
        if move == 3: self.plpos = 2
        for i in range(36):
            for j in range(0, 9):
                self.disp[i][j] = 0
        if self.it == 0: self.op[0] = random.randint(1,2)
        if self.it == 11: self.op[1] = random.randint(1,2)
        if self.it == 22: self.op[2] = random.randint(1,2)
        self.printCars(self.it, self.op[0], self.op[1], self.op[2], self.plpos)
        for i in range(3, 23):
            if i%3 != self.sideit:
                self.disp[i][0] = 1
                self.disp[i][9] = 1
            else:
                self.disp[i][0] = 0
                self.disp[i][9] = 0
        ptGain=0
        if self.it == 23 and self.op[0] > -1: ptGain = 1
        if (self.it+11)%33 == 23 and self.op[2] > -1: ptGain = 1
        if (self.it+22)%33 == 23 and self.op[2] > -1: ptGain = 1
        self.score = self.score + ptGain
        rew = 1.0
        if (self.it in range(16,23) and self.plpos==self.op[0]) or (self.it in range(27,34) and self.plpos==self.op[1]) or (self.it in range(4,12) and self.plpos==self.op[2]):
            rew = -2.0
        self.it = self.it + 1
        if self.it == 33: self.it = 0
        self.sideit = self.sideit + 1
        if self.sideit == 3: self.sideit = 0
        return rew

    # Return board state
    def getBoard(self): return list(self.disp[3:23])

    def getScore(self): return self.score

def printScr(disp, score, its, t, alive=0):
    clear()
    print 'Its:', its, 'Time:', t, alive
    print 'Your score is:', score
    for i in range(20):
        for j in range(10):
            if disp[i][j] == 0: print ' ',
            else: print '#',
        print

# Algorithm that choses optimal actions
class QLearner:
    # Reseting AI's parametres
    def __init__(self, vdict, att):
        self.vDict = vdict
        self.petnica = []
        self.preA = -1
        self.actionToTest = att

    # Generate AI's move based on current board state and training data
    def getMove(self, scr, mode):
        #print self.vDict[boardHash][index][1]
        actions = [1, 2, 3]
        boardHash = HashState(scr)
        if not boardHash in self.vDict.keys():
            self.preA = random.choice(actions)
            #print 'aaa'
            #getch()
        else:
            #print 'bbb'
            #getch()
            actions = []
            for i in range(3):
                if self.vDict[boardHash][i] == True: actions.append(i+1)
            if len(actions) == 0:
                self.preA = 2
                #print 'ccc'
                #getch()
            else:
                self.preA = random.choice(actions)
                #print 'ddd'
                #getch()
        #self.petnica.append([boardHash, index, self.preA-1])
        return self.preA


    # Evaluating learners reward
    def giveRew(self, status, scr, move):
        #for s in list(reversed(self.petnica)):
        boardHash = HashState(scr)
        index = 0
        if status < 0:
            if not boardHash in self.vDict.keys():
                self.actionToTest[boardHash] = []
                self.actionToTest[boardHash].append(0)
                self.vDict[boardHash] = [True for i in range(3)]
                #print 'NEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEW'
                #getch()
            """for i in range(len(self.vDict[boardHash])):
                if scr == self.vDict[boardHash][index][0]:
                    index = i"""
            #if self.actionToTest[boardHash][index] < 3:
            self.vDict[boardHash][move] = False
            #print self.vDict[boardHash]
            #getch()
                #self.actionToTest[boardHash][move-1] = self.actionToTest[boardHash][move-1] + 1
            #break

########################################################
                
            """if status > 0 and toosmall < 2:
                # For positive reward
                for i in range(3):
                    if i == s[2]:
                        self.vDict[s[0]][s[1]][1][i] = (1-(status/64))*self.vDict[s[0]][s[1]][1][i] + 48*status
                    else:
                        self.vDict[s[0]][s[1]][1][i] = self.vDict[s[0]][s[1]][1][i]*(1-(status/64))
            elif toosmall < 2:
                # For negative reward
                for i in range(3):
                    if i != s[2]:
                        if 3*1024-self.vDict[s[0]][s[1]][1][s[2]] == 0:
                            print 3*1024-self.vDict[s[0]][s[1]][1][s[2]], s[0], s[1], s[2]
                        self.vDict[s[0]][s[1]][1][i] = self.vDict[s[0]][s[1]][1][i]*(1+(-status*self.vDict[s[0]][s[1]][1][s[2]])/(64*(3*1024-self.vDict[s[0]][s[1]][1][s[2]])))
                self.vDict[s[0]][s[1]][1][s[2]] = self.vDict[s[0]][s[1]][1][s[2]]*(1-(-status/64))
            # Decreasing status before rewarding next state (previous)
            status = status / 2
            if status == 1: break"""
    
    # Function called by parent modul
    """
     mode:
     1 - single player
     2 - AI for showing
     3 - training Ai - hiden screen
    """
mode = 3
mins = 1
maxScore = 0
its = 1
vDict = {}
aTT = {}
print 'Start'
# Loading generated training data if it exists
if os.path.exists('trainingFile.npy'):
    loadList = np.load('trainingFile.npy').tolist()
    #print loadList[0]
    vDict.clear()
    for inst in loadList:
        vDict[inst[1]] = inst[0]
        aTT[inst[1]] = []
        for h in inst: aTT[inst[1]].append(0) 
    print 'vDict loaded.'
    #print vDict
# Iterating for fixed time
start = time.clock()
while time.clock()-start < mins * 60:
    # Printing current state of game counters
    if its % 1000 == 0: print its, time.clock()-start
    game = RacingGame()
    qLearner = QLearner(vDict, aTT)
    alive = 0
    move = 2
    board = game.getBoard()
    game.makeMove(move)
    #if mode < 3:
    #    printScr(game.getBoard(), 0, its, 0)
    while alive >= 0 and time.clock()-start < mins * 60:
        prevMove = move
        move = 2
        prevBoard = [[0 for i in range(10)] for j in range(20)]
        for i in range(20):
            for j in range(10):
                prevBoard[i][j] = board[i][j]
        #prevBoard = []  list(board)
        if mode == 1:
            inp = 'e'
            while (not inp in ['a', 's', 'd']): inp = getch()
            if inp == 'a': move = 1
            elif inp == 'd': move = 3
            else: move = 2
        elif mode in [2,3]:
            move = qLearner.getMove(prevBoard, mode) # Calculating move for this iteration

        alive = game.makeMove(move) # Current board state in game object changed here
        score = game.getScore()
        #print board
        #board = list(game.getBoard())
        #print board
        #getch()
        if score > maxScore:
            maxScore = score
        if mode < 3:
            printScr(board, game.getScore(), its, time.clock()-start, alive)
            print len(vDict)
        #if mode == 3:
        qLearner.giveRew(alive, prevBoard, move-1)
        #for v in vDict: print v
        #print prevMove, move, HashState(board), HashState(prevBoard)
    f = open ('Scores.txt', 'a')
    f.write(str(game.getScore())+' ')
    f.close()
    its = its + 1
    #print 'Kraj!'
    #getch()
f = open ('Scores.txt', 'a')
f.write('\n')
f.close()
print 'maxScore:', maxScore
saveList = [(v, k) for k, v in vDict.iteritems()]
#np.save('trainingFile', saveList)
print 'trainingFile saved'
