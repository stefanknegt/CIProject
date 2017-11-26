import pickle
from keras.utils import np_utils
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Flatten
import csv
import numpy as np
from sklearn.model_selection import train_test_split

def str_to_float_with_precision(item):
    precision = 2
    return round(float(item),2)

def load_data():
    files = ['Data/finalBerni.txt']
    for f in files:
        data = np.genfromtxt(f, delimiter=' ')
        first = False
    return data

def train_mlp(x_train,y_train,x_test,y_test):
    features = x_train.shape[1]


    model = Sequential()
    model.add(Dense(100, input_dim=features,activation='sigmoid'))
    #Add hidden layer
    model.add(Dense(100, activation='sigmoid'))
    model.add(Dense(100, activation='sigmoid'))
    #Add output layer with 1 node to output either 0 or 1
    model.add(Dense(3,activation='tanh'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    print(model.summary())

    #fit the model
    model.fit(x_train, y_train, epochs=50,verbose=1)

    # Final evaluation of the model
    print(model.evaluate(x=x_test, y=y_test, verbose=1))
    model.save('3layerMLPBERNI.h5')

def train_rnn(x_train,y_train,x_test,y_test):
    model.add(Dense(22*timesteps,input_shape=(TimeSteps,Features),activation = "tanh"))
    model.add(SimpleRNN(2,activation = "tanh"))
    model.add(Dense(1,activation = "tanh"))

def load_keras_model(modelname):

    newmodel = load_model(modelname)
    return newmodel

def predict_output(model,input_data):
    #print(input_data)
    input_data = np.reshape(input_data,(1,22))
    output = model.predict(input_data)
    return float(output[:,0]),float(output[:,1]),float(output[:,2])

#input_data = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]]
#output_data = [[2,2],[4,4],[6,6],[8,8],[9,9],[10,10],[12,12]]

#train_mlp(input_data,output_data)
data = load_data()
y = data[:,0:3]
x = data[:,3:]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, random_state=42)
print(x_train.shape,y_train.shape)
train_mlp(x_train,y_train,x_test,y_test)
#currentModel = load_keras_model('MLP.h5')
#print(predict_output(currentModel,x_test[1]))
