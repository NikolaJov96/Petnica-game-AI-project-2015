# game - Racing
# var: 2

import os
import sys
from msvcrt import getch
import random
import numpy as np
import time
clear = lambda: os.system('cls')

# Load random bitstrings
rndBitS = np.load('BitStrings.npy')
# Function that hashes board states
def HashState(scr):
    h = 0
    for i in range(20):
        for j in range(10):
            if scr[i][j] != 0:
                h = h ^ rndBitS[3*i+j]
    return h

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
        rew = 0
        if ptGain > 0: rew = 8.0
        if (self.it in range(16,23) and self.plpos==self.op[0]) or (self.it in range(27,34) and self.plpos==self.op[1]) or (self.it in range(4,12) and self.plpos==self.op[2]):
            rew = -8.0
        self.it = self.it + 1
        if self.it == 33: self.it = 0
        self.sideit = self.sideit + 1
        if self.sideit == 3: self.sideit = 0
        return rew

    # Return board state
    def getBoard(self): return self.disp

    def getScore(self): return self.score

def printScr(disp, score, its, t):
    clear()
    print 'Its:', its, 'Time:', t
    print 'Your score is:', score
    for i in range(3, 23):
        for j in range(0,10):
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
    def makeMove(self, scr, mode):
        # Hashing board state
        boardHash = HashState(scr)
        index = 0
        if not boardHash in self.vDict.keys():
            self.actionToTest[boardHash] = []
            self.actionToTest[boardHash].append(0)
            self.vDict[boardHash] = []
            self.vDict[boardHash].append([scr, [1024 for i in range(3)]])
        for i in range(len(self.vDict[boardHash])):
            if scr == self.vDict[boardHash][index][0]:
                index = i
        #print self.vDict[boardHash][index][1]
        actions = [1, 2, 3]
        if mode == 3:
            if not boardHash in self.vDict.keys():
                self.actionToTest[boardHash][index] = 0
                self.vDict[boardHash][index] = [scr, [1024 for i in range(3)]]
            if self.actionToTest[boardHash][index] == 3:
                #self.actionToTest[boardHash][index] = random.randint(0, 3)
                rnd = random.randint(0, 3*1024)
                su = 0
                for a in actions:
                    su = su + self.vDict[boardHash][index][1][a-1]
                    if rnd <= su:
                        self.preA = a
                        break
            else:
                self.preA = self.actionToTest[boardHash][index] + 1
                self.actionToTest[boardHash][index] = self.actionToTest[boardHash][index] + 1
            #if self.actionToTest[boardHash][index] == 3: self.actionToTest[boardHash][index] = 0
        elif mode == 2:
            self.preA = self.vDict[boardHash][index][1].index(max(self.vDict[boardHash][index][1])) + 1
            #self.preA = -1
            #for i in range(0,3):
            #    if self.vDict[boardHash][index][1][i] > self.vDict[boardHash][index][1][self.preA-1]:
            #        self.preA = i+1
        self.petnica.append([boardHash, index, self.preA-1])
        return self.preA


    # Evaluating learners reward
    def giveRew(self, status):
        for s in list(reversed(self.petnica)):
            toosmall = 0
            for i in self.vDict[s[0]][s[1]][1]:
                if i < 2: toosmall = toosmall + 1
            if status > 0 and toosmall < 2:
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
            if status == 1: break
    
    # Function called by parent modul
    """
     mode:
     1 - single player
     2 - AI for showing
     3 - training Ai - hiden screen
    """
def startGame(mode):
    maxScore = 0
    its = 1
    vDict = {}
    aTT = {}
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
        getch()
    start = time.clock()
    while time.clock()-start < 30 * 60:
        # Printing current state of game counters
        if its % 1000 == 0: print its, time.clock()-start
        game = RacingGame()
        qLearner = QLearner(vDict, aTT)
        alive = 0
        game.makeMove(2)
        if mode < 3:
            printScr(game.getBoard(), 0, its, 0)
        while alive >= 0:
            move = 2
            if mode == 1:
                inp = 'e'
                while (not inp in ['a', 's', 'd']): inp = getch()
                if inp == 'a': move = 1
                elif inp == 'd': move = 3
                else: move = 2
            elif mode in [2,3]:
                move = qLearner.makeMove(game.getBoard(), mode)

            alive = game.makeMove(move)
            score = game.getScore()
            if score > maxScore:
                maxScore = score
            if mode < 3:
                printScr(game.getBoard(), game.getScore(), its, time.clock()-start)
            if mode == 3:
                qLearner.giveRew(alive)

        its = its + 1
        #print 'Kraj!'
        #getch()

    print 'maxScore:', maxScore
    saveList = [(v, k) for k, v in vDict.iteritems()]
    np.save('trainingFile', saveList)
    print 'trainingFile saved'
