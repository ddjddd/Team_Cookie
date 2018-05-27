a = [[1,100],[3,4]]

a = sorted(a, key=lambda x: x[-1])

print(a)
import numpy as np
b= np.array(([1,2,3],[100,200,300],[1,1,1]),dtype=np.int)
c= np.array(([11,12,13],[1100,2100,3100],[11,11,11]),dtype=np.int)
print(b)
b[1][1]=100000
print(b[1][1])


import random

a, b=random.sample(range(0, 2), 2)
print(a, b)


from keras.models import Sequential
from keras.layers import Dense
import numpy as np
model = Sequential()
model.add(Dense(units=32, activation='tanh', input_dim=4, use_bias=False))
model.add(Dense(units=16, activation='tanh', input_dim=108, use_bias=False))
model.add(Dense(units=3, activation='softmax', use_bias=False))

a = np.array([1, 2, 3, 4])
b=np.array([a])
#a = np.array(a)
print(b.shape)
b = model.predict(b)
print(b)