import pickle
from keras.utils import np_utils
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, LSTM, Input, merge
import csv
import numpy as np
from sklearn.model_selection import train_test_split

def str_to_float_with_precision(item):
    precision = 2
    return round(float(item),2)

def load_data():
    files = ['aalborg.csv']#'f-speedway.csv','alpine-1.csv',
    first = True
    for f in files:
        data = np.genfromtxt(f, delimiter=',')
        if first is False:
            data = np.concatenate((data,np.genfromtxt(f, delimiter=',')),axis=0)
        first = False
    return data

def train_mlp(x_train,y_train,x_test,y_test):
    features = x_train.shape[1]
    x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
    x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
    model = Sequential()
    model.add(LSTM(200, input_shape = (1, features)))
    model.add(Dense(100, activation='elu'))
    model.add(Dense(3, activation='elu'))
    model.compile(loss="mean_squared_error", optimizer="adam")
    '''
    input_lay = Input(shape=(features,))
    h1 = LSTM(100)(input_lay)
    #h2 = Dense(100, activation = 'sigmoid')(h1)
    steering = Dense(1,activation='tanh')(h2)
    accelerator = Dense(1, activation='sigmoid')(h2)
    breaking = Dense(1, activation='sigmoid')(h2)
    output_lay = merge([steering, accelerator, breaking],mode='concat')
    model = Model(input=input_lay, output=output_lay)
    model.compile(loss='mean_squared_error', optimizer='adam')'''
    print(model.summary())

    #fit the model
    model.fit(x_train, y_train, batch_size=5, epochs=30,verbose=1)

    # Final evaluation of the model
    print(model.evaluate(x=x_test, y=y_test, batch_size=1, verbose=1))
    model.save('MLPL.h5')

def load_keras_model(modelname):

    newmodel = load_model(modelname)
    return newmodel

def predict_output(model,input_data):
    print(input_data)
    input_data = np.reshape(input_data,(1,22))
    output = model.predict(input_data)
    return float(output[:,0]),float(output[:,1]),float(output[:,2])

#input_data = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]]
#output_data = [[2,2],[4,4],[6,6],[8,8],[9,9],[10,10],[12,12]]

#train_mlp(input_data,output_data)
data = load_data()
y = data[:,0:3]
#print(y)
x = data[:,3:]
#print(x)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)
#print(x.shape,y.shape)
train_mlp(x_train,y_train,x_test,y_test)
#currentModel = load_keras_model('MLP.h5')
#print(predict_output(currentModel,x_test[1]))
