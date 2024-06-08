import random
import numpy as np

arr = [0 for i in range(200)]
for i in range(200):
    arr[i] = random.randint(0, 100000)
np.save('BitStrings', arr)
