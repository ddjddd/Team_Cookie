from keras.models import Sequential
from keras.layers import Dense
import random



weights_list2=[]
weights_list3=[]
weights_list4=[]
generatnion1 = []

for ii in range(4):
    weights_list = []
    model = Sequential()
    model.add(Dense(units=32, activation='tanh', input_dim=108,use_bias=False))
    model.add(Dense(units=16, activation='tanh', input_dim=108, use_bias=False))
    model.add(Dense(units=3, activation='softmax', use_bias=False))

    for layer in model.layers:
        weights = layer.get_weights()[0] # list of numpy arrays
        weights_list.append(weights)
    generatnion1.append((weights_list,999))

print(generatnion1[0][0][0])
#print(generatnion1)
#print(len(generatnion1))
#     print(weights.shape )
#
# print(len(weights_list)) # 3

def pick2(group):
    population = len(group)
    picked = random.sample(range(0,population), 2)
    return group[picked[0]],group[picked[1]]


def cross_over(a, b):
    layer_num = len(a)
    #print(a[1])
    #print(layer_num)
    new_creature=[]
    for i in range(layer_num):
        a_i = a[0][i].copy()
        b_i = b[0][i].copy()
        #print(a_i)
        shape = a_i.shape
        for k in range (shape[0]):
            for j in range(shape[1]):
                selecta, selectb =  random.sample(range(0,2), 2)
                a_i[k][j] = selecta * a_i[k][j] + selectb * b_i[k][j]
        new_creature.append(a_i)
    return new_creature




def generation_change(generation, survive_rate, mutation_rate): # generation = [  (weights_lists, fittness),(), (), ()........]
    population = len(generation)
    survive_population = int (population * survive_rate)
    generation = sorted(generation, key=lambda x: x[-1], reverse=True)
    next_generation = []

    # selection
    for i in range(survive_population):
        next_generation.append(generation[i])

    # cross_over
    temp_generation = []
    for i in range(population-survive_population):
        a, b  = pick2(next_generation)
        new_creature = cross_over(a,b)
        temp_generation.append((new_creature,0) )
    next_generation = next_generation + temp_generation # concat

    # mutation


    return next_generation



newgen = generation_change(generatnion1,0.5,0)
#print(newgen)
#print(len(newgen))

print("--------------")
print(newgen[0][0][0])
#print(newgen[1])
    #mutations







