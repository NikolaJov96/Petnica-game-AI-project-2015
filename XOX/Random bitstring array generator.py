import random
import numpy as np

arr = [[0 for i in range(2)] for j in range(9)]
for i in range(9):
    for j in range(2):
        arr[i][j] = random.randint(0, 100000)
np.save('BitStrings', arr)
