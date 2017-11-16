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
    #files = ['../train_data/f-speedway.csv','../train_data/ovaltracke5.csv','../train_data/f-speedway.csv','../train_data/aalborg.csv','../train_data/alpine-1.csv','../train_data/Alpine1.csv','../train_data/Alpine2.csv','../train_data/Brondehach.csv','../train_data/E-road.csv','../train_data/E-track1.csv','../train_data/E-track3.csv','../train_data/Olethros-road1.csv','../train_data/Ruudskogen.csv','../train_data/Wheel1.csv','../train_data/Wheel2.csv']
    #files = ['../train_data/f-speedway.csv','../train_data/aalborg.csv','../train_data/alpine-1.csv','../train_data/Alpine1.csv','../train_data/Alpine2.csv']
    files = ['../train_data/Spring.csv','../train_data/Alpine1.csv','../train_data/Alpine2.csv','../train_data/Brondehach.csv','../train_data/CGtrack3.csv','../train_data/E-road.csv','../train_data/Etrack2.csv','../train_data/Etrack3.csv','../train_data/Etrack4.csv','../train_data/Etrack6.csv','../train_data/olethros1.csv','../train_data/Wheel2.csv','../train_data/Spring.csv']
    first = True
    for f in files:
        data = np.genfromtxt(f, delimiter=',')
        if first is False:
            data = np.concatenate((data,np.genfromtxt(f, delimiter=',')),axis=0)
        first = False
    return data

def train_nn(x_train,y_train,x_test,y_test,nn_type):
    features = x_train.shape[1]
    if nn_type == "LSTM":
        x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
        x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
        model = Sequential()
        model.add(LSTM(200, input_shape = (1, features)))
        model.add(Dense(100, activation='elu'))
        model.add(Dense(3, activation='elu'))
    elif nn_type == "LSTM_var_activ":
        input_lay = Input(sermhape=(features,))
        h1 = LSTM(100)(input_lay)
        h2 = Dense(100, activation = 'sigmoid')(h1)
        steering = Dense(1,activation='tanh')(h2)
        accelerator = Dense(1, activation='sigmoid')(h2)
        breaking = Dense(1, activation='sigmoid')(h2)
        output_lay = merge([steering, accelerator, breaking],mode='concat')
        model = Model(input=input_lay, output=output_lay)
    elif nn_type == "Dense":
        model = Sequential()
        model.add(Dense(100, input_dim=features,activation='sigmoid')) #word vector size 32
        #model.add(Dense(100, activation='sigmoid'))
        #Add output layer with 1 node to output either 0 or 1
        model.add(Dense(3,activation='tanh'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    print(model.summary())
    #fit the model
    model.fit(x_train, y_train, epochs=100,verbose=1)
    # Final evaluation of the model
    print(model.evaluate(x=x_test, y=y_test, batch_size=None, verbose=1))
    model.save('Dense_All.h5')

def load_keras_model(modelname):
    newmodel = load_model(modelname)
    return newmodel

def predict_output(model,input_data, nn_type):
    print(input_data)
    if nn_type == "LSTM":
        input_data = np.reshape(input_data,(1,1,22))
    else:
        input_data = np.reshape(input_data,(1,22))
    output = model.predict(input_data)
    return float(output[:,0]),float(output[:,1]),float(output[:,2])

data = load_data()
y = data[:,0:3]
x = data[:,3:]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)
#print(x_train.shape,y_train.shape)
train_nn(x,y,x_test,y_test,nn_type = "Dense")
#currentModel = load_keras_model('MLP.h5')
#print(predict_output(currentModel,x_test[1]))
