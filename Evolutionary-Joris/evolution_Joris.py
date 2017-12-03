import numpy as np
import shutil
import os
import time
import wrapper
import signal

def create_new_models():

    # Remove the old laptimes.txt
    os.remove('laptimes.txt')

    # Make sure there is always a laptime.txt
    with open ('laptimes.txt','w') as new_file:
        new_file.write(str(0) + '\n')
        new_file.close()

    with open ('best_param.txt','r') as file:
        lines = file.readlines()
        k = float(lines[0])
        x_diff = float(lines[1])
        c = float(lines[2])
        D = float(lines[3])
        return k,x_diff,c,D


def create_new_children(population):
    k, x_diff, c, D = create_new_models()
    for i in range(population):

        k_child = k + np.random.normal(0.0,0.1)
        x_diff_child = x_diff + np.random.normal(0.0,2.5)
        c_child = c + np.random.normal(0.0,0.0005)
        D_child = D + np.random.normal(0.0,3.5)

        filename = 'child'+str(i)+'.txt'

        with open ('Joris-Evolution/'+ filename,'w') as child:
            child.write(str(k_child) + '\n')
            child.write(str(x_diff_child) + '\n')
            child.write(str(c_child) + '\n')
            child.write(str(D_child) + '\n')
            child.close()
    return

def get_file_length(file_name):
    length = open(file_name,'r')
    length = length.readlines()
    return len(length)

def train(population):
    for i in range (population):
        filename = 'child'+str(i) + '.txt'
        shutil.copy(os.path.join('Joris-Evolution',filename),os.path.join('best_param.txt'))

        for i in range(0,4):
            previous_length = get_file_length('laptimes.txt')
            wrapper.train(i)

            time.sleep(15)
            os.system('pkill xterm') # kill all xterm

            laptimes = open('laptimes.txt', 'r')
            lap_times = laptimes.readlines()
            lap_times = [x.strip() for x in lap_times]
            print(lap_times)
            lines = len(lap_times)
            if lines < i*4+1:
                laptimes = open('laptimes.txt', 'a')
                laptimes.write("300000 \n")
    return True

def evaluate_fitness():
    with open ('laptimes.txt','r') as f:

        lines = f.readlines()

        if len(lines)-1 % 4 != 0:
            raise ValueError ('Not enough data points, something went wrong')

        avg_list = []

        for i in range(1,len(lines),4):
            avg = float(lines[i]) + float(lines[i+1]) +float(lines[i+2]) + float(lines[i+3])
            avg /= population
            avg_list.append(avg)

        best = avg_list.index((min(avg_list)))

        print ('The best child is',best)

        filename = 'child' + str(best) +'.txt'
        os.remove(os.path.join('best_param.txt'))
        shutil.copy(os.path.join('Joris-Evolution',filename),os.path.join('best_param.txt'))
        print ('Done with one copy!')

def run(num_epochs):
    for epoch in range(0,num_epochs):
        create_new_children(population)
        trained = train(population)
        evaluate_fitness()
        print ('Done with epoch',epoch+1)
    return True

population = 5
num_epochs = 5

bool = run(num_epochs)

