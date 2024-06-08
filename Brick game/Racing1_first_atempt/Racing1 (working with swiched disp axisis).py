# game - Racing
# ver: 1

import os
import time
import random
import math
from msvcrt import getch
import time
import numpy as np

def startGame(mode):
    disp = [[0 for i in range(0, 36)] for j in range(0, 10)]

    if mode == 2:
        from Racing1ai import genMove
    
    def printCars(ite, c0, c1, c2, me):     #printing all cars
        
        def printCar(x, y):     #printing each car
            disp[x][y]=1
            disp[x-1][y+1]=1
            disp[x][y+1]=1
            disp[x+1][y+1]=1
            disp[x][y+2]=1
            disp[x-1][y+3]=1
            disp[x][y+3]=1
            disp[x+1][y+3]=1
        
        if c0>-1: printCar(c0*3, ite)
        if c1>-1: printCar(c1*3, (ite+22)%33)
        if c2>-1: printCar(c2*3, (ite+11)%33)
        printCar(me*3, 19)

    score = 0
    it = -1
    sideit = 0
    self = 1
    op = [-1, -1, -1]
    for i in range(3, 23):
        if (i%3 == 0) or (i%3 == 1):
            disp[0][i] = 1
            disp[9][i] = 1
    crash = False
    lvl = 1
    trSetList = []
    
    while not crash:
        for i in range(0, 9):
            for j in range(36):
                disp[i][j] = 0
        if it == 0: op[0] = random.randint(1,2)
        if it == 11: op[1] = random.randint(1,2)
        if it == 22: op[2] = random.randint(1,2)
        printCars(it, op[0], op[1], op[2], self)
        for i in range(3, 23):
            if i%3 != sideit:
                disp[0][i] = 1
                disp[9][i] = 1
            else:
                disp[0][i] = 0
                disp[9][i] = 0
        #printscr
        clear = lambda: os.system('cls')
        clear()
        print 'Your score is:', score
        for j in range(3, 23):
            for i in range(0,10):
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
            break
        it=it+1
        if it==33: it=0
        sideit=sideit+1
        if sideit==3: sideit=0
        inp = 'e'
        st = time.time()
        en = st
        while (not inp in ['a', 's', 'd']) and (en-st<100):
            if mode == 1:
                inp = getch()
                #save trening set
                trDisp = [[disp[i][j] for i in range(10)] for j in range(3,23)]
                trSetList.append([trDisp, ptGain, inp])
            else: inp = genMove(disp, ptGain)
            en = time.time()
        if inp == 'a': self = 1
        if inp == 'd': self = 2
        inp = 'e'
    if mode == 2: genMove(dips, -10)
    print 'GAME OVER'
    np.save('trainingFile', trSetList)
    input



















                        
