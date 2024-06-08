import numpy as np
import random

inputs = np.load('trainingFile.npy')

co1 = [[random.random() for i in range(400)] for j in range(201)]
co2 = [random.random() for i in range(400)]
m = [0 for i in range(400)]

for scr in inputs:
    dis = np.array(scr[0])
    disp = [ item for innerlist in dis for item in innerlist ]
    r = scr[1]
    a = 1
    if scr[2]=='d': a = 2
    for i in range(400):
        m[i] = 0
        for j in range(200):
            m[i] = m[i] + disp[j]*co1[j][i]
        m[i] = m[i] + a*co1[j][200]
    out = 0
    for i in range(400):
        out+=m[i]*co2[i]
    print out
