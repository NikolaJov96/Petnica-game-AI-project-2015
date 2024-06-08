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
    op = [(-1, -1), (-1, -1), (-1, -1)]
    for i in range(3, 23):
        if (i%3 == 0) or (i%3 == 1):
            #disp[i][0] = 1
            disp[i][9] = 1
            
    # Reseting game if needed
    def __init__(self):
        self.disp = [[0 for i in range(10)] for j in range(36)]
        self.score = 0
        self.it = -1
        self.sideit = 0
        self.plpos = 1
        self.op = [[-1, -1], [-1, -1], [-1, -1]]
        for i in range(3, 23):
            if (i%3 == 0) or (i%3 == 1):
                #self.disp[i][0] = 1
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

    def printCars(self, ite, c00, c01, c10, c11, c20, c21, me):     #printing all cars
        if c00>-1: self.printCar(ite, c00*3+1)
        if c01>-1: self.printCar(ite, c01*3+1)
        if c10>-1: self.printCar((ite+22)%33, c10*3+1)
        if c11>-1: self.printCar((ite+22)%33, c11*3+1)
        if c20>-1: self.printCar((ite+11)%33, c20*3+1)
        if c21>-1: self.printCar((ite+11)%33, c21*3+1)
        self.printCar(19, me*3+1)

    # Submitting move and calculating all movements
    def makeMove(self, move):
        if move == 1 and self.plpos != 0: self.plpos = self.plpos - 1
        if move == 3 and self.plpos != 2: self.plpos = self.plpos + 1
        for i in range(36):
            for j in range(0, 9):
                self.disp[i][j] = 0
        if self.it == 0:
            acts = [0,1,2]
            self.op[0][0] = random.choice(acts)
            acts.remove(self.op[0][0])
            self.op[0][1] = random.choice(acts)
        if self.it == 11:
            acts = [0,1,2]
            self.op[1][0] = random.choice(acts)
            acts.remove(self.op[1][0])
            self.op[1][1] = random.choice(acts)
        if self.it == 22:
            acts = [0,1,2]
            self.op[2][0] = random.choice(acts)
            acts.remove(self.op[2][0])
            self.op[2][1] = random.choice(acts)
        self.printCars(self.it, self.op[0][0], self.op[0][1], self.op[1][0], self.op[1][1], self.op[2][0], self.op[2][1], self.plpos)
        for i in range(3, 23):
            if i%3 != self.sideit:
                #self.disp[i][0] = 1
                self.disp[i][9] = 1
            else:
                #self.disp[i][0] = 0
                self.disp[i][9] = 0
        ptGain=0
        if self.it == 23 and self.op[0][0] > -1: ptGain = 1
        if (self.it+11)%33 == 23 and self.op[2][0] > -1: ptGain = 1
        if (self.it+22)%33 == 23 and self.op[2][0] > -1: ptGain = 1
        self.score = self.score + ptGain
        rew = 1.0
        if (self.it in range(16,23) and (self.plpos==self.op[0][0] or self.plpos==self.op[0][1])):
            rew = -2.0
        if (self.it in range(27,34) and (self.plpos==self.op[1][0] or self.plpos==self.op[1][1])):
            rew = -2.0
        if (self.it in range(4,12) and (self.plpos==self.op[2][0] or self.plpos==self.op[2][1])):
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
        else:
            actions = []
            for i in range(3):
                if self.vDict[boardHash][i] == True: actions.append(i+1)
            if len(actions) == 0:
                self.preA = 2
            else:
                self.preA = random.choice(actions)
        #self.petnica.append([boardHash, index, self.preA-1])
        return self.preA


    # Evaluating learners reward
    def giveRew(self, status, scr, move, prevScr, prevMove):
        #for s in list(reversed(self.petnica)):
        boardHash = HashState(scr)
        if status < 0:
            if not boardHash in self.vDict.keys():
                self.actionToTest[boardHash] = []
                self.actionToTest[boardHash].append(0)
                self.vDict[boardHash] = [True for i in range(3)]
            self.vDict[boardHash][move] = False
            if not True in self.vDict[boardHash]:
                boardHash = HashState(prevScr)
                if status < 0:
                    if not boardHash in self.vDict.keys():
                        self.actionToTest[boardHash] = []
                        self.actionToTest[boardHash].append(0)
                        self.vDict[boardHash] = [True for i in range(3)]
                    self.vDict[boardHash][prevMove] = False
""" mode:
 1 - single player
 2 - AI for showing
 3 - training Ai - hiden screen
"""
mode = 3
mins = 0.5
maxScore = 0
its = 1
vDict = {}
aTT = {}
print 'Start'
f = open('Scores.txt', 'ab')
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
    prevBoard1 = [[0 for i in range(10)] for j in range(20)]
    for i in range(20):
        for j in range(10):
            prevBoard1[i][j] = board[i][j]
    game.makeMove(move)
    #if mode < 3:
    #    printScr(game.getBoard(), 0, its, 0)
    while alive >= 0 and time.clock()-start < mins * 60:
        prevMove = move
        move = 2
        prevBoard2 = [[0 for i in range(10)] for j in range(20)]
        for i in range(20):
            for j in range(10):
                prevBoard2[i][j] = prevBoard1[i][j]
        prevBoard1 = [[0 for i in range(10)] for j in range(20)]
        for i in range(20):
            for j in range(10):
                prevBoard1[i][j] = board[i][j]
        if mode == 1:
            inp = 'e'
            while (not inp in ['a', 's', 'd']): inp = getch()
            if inp == 'a': move = 1
            elif inp == 'd': move = 3
            else: move = 2
        elif mode in [2,3]:
            move = qLearner.getMove(prevBoard1, mode) # Calculating move for this iteration

        alive = game.makeMove(move) # Current board state in game object changed here
        score = game.getScore()
        if score > maxScore:
            maxScore = score
        if mode < 3:
            printScr(board, game.getScore(), its, time.clock()-start, alive)
        if mode in [2]: print len(vDict)
        if mode > 1: qLearner.giveRew(alive, prevBoard1, move-1, prevBoard2, prevMove-1)
        #for v in vDict: print v
        #print prevMove, move, HashState(board), HashState(prevBoard)
    #f = open('Scores.txt', 'a')
    f.write(str(game.getScore())+' ')
    #f.close()
    its = its + 1
    #print 'Kraj!'
    #getch()
#f = open('Scores.txt', 'a')
f.write('\n')
f.close()

print 'maxScore:', maxScore
saveList = [(v, k) for k, v in vDict.iteritems()]
#np.save('trainingFile', saveList)
print 'trainingFile saved'
