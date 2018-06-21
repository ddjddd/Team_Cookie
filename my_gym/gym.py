import sqlite3
import numpy as np
# import pandas as pd
from sklearn import preprocessing
from mat_generator import rmatrix, null_matrix
import random

import emulator

# columns = ['ratio', 'amount', 'ends', 'foreigner', 'insti', 'person', 'program', 'credit']
input_size = 9*12

# 0: jump
# 1: slide
# 2: do nothing
action_space = [0, 1, 2]

isTestMode = False

# " isTest: training모드일때는 false, test모드일때는 true"
def reset(isTest=False):
    # global index, earn, deposit, buy, isTestMode

    # state = []
    # for col in columns:
    #     state.append( cur[col] )
    # state.append( deposit )

    state = null_matrix()

    return state

# state, reward, done, _
def step(action):
    global earn
    # global index, earn, deposit, buy, buy_cost
    reward = 0
    done = False

    if action==0: #####JUMP
        emulator.cookie_jump(852, 480)

    elif action==1: #####SLIDE
        emulator.cookie_slide(852, 480)

    elif action == 2: ####DO NOTHING
        emulator.cookie_donothing(852, 480)


    earn += reward

    done = True if (random.random() < 0.1) else False

    return [state, reward, done, None]


