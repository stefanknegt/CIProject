import numpy as np
import shutil
import os
import time
import wrapper
import signal
import matplotlib.pyplot as plt

def initialize_models(population):

    for i in range(population):
        k = np.random.uniform(0,3)
        x_diff = np.random.uniform(0,200)
        c = np.random.uniform(0,0.1)
        D = np.random.uniform(0,200)
        track_dev = np.random.uniform(-2,2)

        filename = 'child'+str(i)+'.txt'
        with open ('Joris-Evolution/'+ filename,'w') as child:
            child.write(str(k) + '\n')
            child.write(str(x_diff) + '\n')
            child.write(str(c) + '\n')
            child.write(str(D) + '\n')
            child.write(str(track_dev) + '\n')
            child.close()

def reinitialize_laptimes():     # Make sure there is always a laptime.txt
    os.remove('laptimes.txt')

    with open('laptimes.txt', 'w') as new_file:
        new_file.write(str(0) + '\n')
        new_file.close()

    return

def create_new_child(file_to_copy,file_name,noise_factor):

    with open ('Joris-Evolution/'+file_to_copy,'r') as parent: # Open the parent
        lines = parent.readlines()

        k = float(lines[0])
        x_diff = float(lines[1])
        c = float(lines[2])
        D = float(lines[3])
        track_dev = float(lines[4])

    k_child = k + np.random.normal(0.0,0.2/noise_factor)
    x_diff_child = x_diff + np.random.normal(0.0,4.0/noise_factor)
    c_child = c + np.random.normal(0.0,0.001/noise_factor)
    D_child = D + np.random.normal(0.0,7.0/noise_factor)
    track_dev_child = track_dev + np.random.normal(0,0.5/noise_factor)

    with open ('Joris-Evolution/'+ file_name,'w') as child:
        child.write(str(k_child) + '\n')
        child.write(str(x_diff_child) + '\n')
        child.write(str(c_child) + '\n')
        child.write(str(D_child) + '\n')
        child.write(str(track_dev_child) + '\n')
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

        for i in range(0,5):
            previous_length = get_file_length('laptimes.txt')
            wrapper.train(i)

            time.sleep(12)
            os.system('pkill xterm') # kill all xterm

            new_length = get_file_length('laptimes.txt')

            if previous_length == new_length:
                laptimes = open('laptimes.txt', 'a')
                laptimes.write("3000000 \n")

            laptimes = open('laptimes.txt', 'r')
            lap_times = laptimes.readlines()
            lap_times = [x.strip() for x in lap_times]
            print(lap_times)

    return True

def evaluate_fitness(best_so_far):
    with open ('laptimes.txt','r') as f:

        lines = f.readlines()

        if (len(lines)-1) % 5 != 0:
            print ('lines (length-1)%4 is',(len(lines)-1)%4)
            raise ValueError ('Not enough data points, something went wrong')

        avg_list = []

        for i in range(1,len(lines),5):
            avg = float(lines[i]) + float(lines[i+1]) +float(lines[i+2]) + float(lines[i+3]) + float(lines[i+4])
            avg /= 5
            avg_list.append(avg)

    best = np.argsort(np.array(avg_list))

    filename = 'child'+str(best[0])+'.txt'
    if min(avg_list) < best_so_far:
        shutil.copy(os.path.join('Joris-Evolution', filename), os.path.join('best_so_far.txt'))
        return best,min(avg_list)

    return best,best_so_far

def reproduce(best,noise_factor):

    model_index = 0
    for i in range(0,4):
        file_to_copy = 'child'+str(best[i])+'.txt'
        for j in range(5):
            filename = 'child'+str(model_index)+'.txt'
            create_new_child(file_to_copy,filename,noise_factor)
            model_index += 1

    print ('Done with making new copies!')
    return

def run(num_epochs,population):

    fitness_over_time = []
    best_fitness = 3000000
    initialize_models(population)

    for epoch in range(0,num_epochs):
        reinitialize_laptimes()
        noise_factor = 1.05**epoch #Noise gets smaller every epoch

        train(population)
        best_indices, best_fitness  = evaluate_fitness(best_fitness)
        reproduce(best_indices,noise_factor)

        fitness_over_time.append(best_fitness)
        print ('Done with epoch',epoch+1)

    plt.plot(np.arange(0,len(fitness_over_time)),fitness_over_time)
    plt.show()
    return

population = 20
num_epochs = 30

run(num_epochs,population)

