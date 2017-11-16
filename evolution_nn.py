import pickle
from keras.utils import np_utils
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Flatten
import numpy as np


def load_keras_model(modelname):
    newmodel = load_model(modelname)
    return newmodel

def get_weights(model):
    n_layers = len(model.layers)
    weights = []
    biases = []
    for i in range(0,n_layers):
        weights.append(model.layers[i].get_weights()[0])
        biases.append(model.layers[i].get_weights()[1])
    biases = model.layers[0].get_weights()[1]
    return weights,biases

def make_childs(w,b):
    n_childs = 2
    for i in range(0,n_childs):
        child = []
        for j in range(0,len(w)):
            noise = np.random.normal(0,0.005,size=w[j].shape)
            new_matrix = np.add(w[j],noise)
            child.append(new_matrix)
        #print(len(child))
        model = Sequential()
        model.add(Dense(100, input_dim=22,activation='sigmoid'))
        #Add hidden layer
        model.add(Dense(100, activation='sigmoid'))
        #Add output layer with 1 node to output either 0 or 1
        model.add(Dense(3,activation='tanh'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        for q in range(0,len(w)):
            print(q)
            model.layers[q].get_weights()[0] = child[q]
            model.layers[q].get_weights()[1] = b[q]
        model.save('EVONN'+str(i)+'.h5')

def make_new_parent(fitness):
    best_10  = sorted(range(len(fitness)), key=lambda i: fitness[i])[-10:]
    for i in range(0,len(best_10)):
        model_name = 'EVON'+str(i)+'.h5'
        model = load_keras_model(model_name)
        weights, bias = get_weights(model)
        for j in range(0,len(weights)):
            new_weights = np.multiply(fitness[i],weights)
    model = Sequential()
    model.add(Dense(100, input_dim=22,activation='sigmoid'))
    #Add hidden layer
    model.add(Dense(100, activation='sigmoid'))
    #Add output layer with 1 node to output either 0 or 1
    model.add(Dense(3,activation='tanh'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for q in range(0,len(weights)):
        print(q)
        model.layers[q].get_weights()[0] = new_weights[q]
        model.layers[q].get_weights()[1] = b[q]
    model.save('NEWBEST.h5')
    new_model = load_keras_model('NEWBEST.h5')
    w, b = get_weights(model)
    make_childs(w,b)



new_model = load_keras_model('MLPLALL4.h5')
w,b = get_weights(new_model)
make_childs(w,b)
