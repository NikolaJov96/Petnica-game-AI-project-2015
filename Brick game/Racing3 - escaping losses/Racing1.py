# game - Racing
# ver: 2

import os
import time
import random
import math
from msvcrt import getch
import time
import numpy as np

def startGame(mode):
    
    disp = [[0 for i in range(0, 10)] for j in range(0, 36)]

    if mode == 2:
        from Racing1ai import genMove
    
    def printCars(ite, c0, c1, c2, me):     #printing all cars
        
        def printCar(x, y):     #printing each car
            disp[x][y]=1
            disp[x+1][y-1]=1
            disp[x+1][y]=1
            disp[x+1][y+1]=1
            disp[x+2][y]=1
            disp[x+3][y-1]=1
            disp[x+3][y]=1
            disp[x+3][y+1]=1
        
        if c0>-1: printCar(ite, c0*3)
        if c1>-1: printCar((ite+22)%33, c1*3)
        if c2>-1: printCar((ite+11)%33, c2*3)
        printCar(19, me*3)

    score = 0
    it = -1
    sideit = 0
    self = 1
    op = [-1, -1, -1]
    for i in range(3, 23):
        if (i%3 == 0) or (i%3 == 1):
            disp[i][0] = 1
            disp[i][9] = 1
    crash = False
    lvl = 1
    import os.path
    if os.path.exists('trainingFile.npy'): trSetList = np.load('trainingFile.npy').tolist()
    else: trSetList = []
    
    while not crash:
        for i in range(36):
            for j in range(0, 9):
                disp[i][j] = 0
        if it == 0: op[0] = random.randint(1,2)
        if it == 11: op[1] = random.randint(1,2)
        if it == 22: op[2] = random.randint(1,2)
        printCars(it, op[0], op[1], op[2], self)
        for i in range(3, 23):
            if i%3 != sideit:
                disp[i][0] = 1
                disp[i][9] = 1
            else:
                disp[i][0] = 0
                disp[i][9] = 0
        #printscr
        if mode == 1:
            clear = lambda: os.system('cls')
            clear()
            print 'Your score is:', score
            for i in range(3, 23):
                for j in range(0,10):
                    if disp[i][j] == 0: print ' ',
                    else: print '#',
                print
        ptGain=0
        if it == 20 and op[0] > -1: ptGain = 1
        if (it+11)%33 == 20 and op[1] > -1: ptGain = 1
        if (it+22)%33 == 20 and op[2] > -1: ptGain = 1
        score = score + ptGain
        if (it in range(16,23) and self==op[0]) or (it in range(27,34) and self==op[1]) or (it in range(4,12) and self==op[2]):
            crash = True
            trDisp = [[disp[i][j] for i in range(3,23)] for j in range(10)]
            trSetList.append([trDisp, -1, 's'])
            break
        it=it+1
        if it==33: it=0
        sideit=sideit+1
        if sideit==3: sideit=0
        inp = 'e'
        while (not inp in ['a', 's', 'd']):
            if mode == 1:
                inp = getch()
            else: inp = genMove(disp, ptGain)
            #save trening set
            trDisp = [[disp[i][j] for i in range(3,23)] for j in range(10)]
            trSetList.append([trDisp, ptGain, inp])
        if inp == 'a': self = 1
        if inp == 'd': self = 2
        inp = 'e'
    #if mode == 2: genMove(dips, -10)
    if mode == 1: print 'GAME OVER'
    np.save('trainingFile', trSetList)
    input



















                        
