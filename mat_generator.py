import random
import numpy as np

# 12*9의 우리 grid와 동일한 크기의 2차원 list matrix를 뽑는다.
def rmatrix():
    matrix = []
    for _ in range(9):
        rand = [random.choice(range(5)) for _ in range(12)]
        matrix += rand
    matrix = np.asarray(matrix)

    return matrix #1차원 배열로 바꿈.
# 1차원 배열로 해야하지는 않을까?

def null_matrix(): #todo: np.arrary 제대로 된거로 바꾸기.
    matrix = []
    for _ in range(9):
        null = [0]*12
        matrix += null
    matrix = np.asarray(matrix)

    return matrix


