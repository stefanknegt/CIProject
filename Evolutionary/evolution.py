import shutil
import os
import wrapper
import time
from evolution_nn import make_childs_new, make_new_parent
import numpy as np
import random
population = 10
best_model = 'Best_Model.h5'
loc = 'EVO_models'
noise = 0.005
if __name__ == "__main__":
    if not os.path.exists(loc):
        os.makedirs(loc)
    make_childs_new(best_model, population, loc, noise)
    open('laptimes.txt', 'w') #delete old results

while True:
    track_id = random.randint(0,3)
    for i in range(population):
        filename = 'EVO'+str(i)+'.h5'
        shutil.copy(os.path.join(loc, filename), os.path.join('EVO_model.h5'))
        circuit_name  = wrapper.train(track_id)
        time.sleep(20)
        print ('trained',filename,'on',circuit_name)
        # os.remove(os.path.join('EVO_model.h5'))
        #check if laptime was registered else DNF

        laptimes = open('laptimes.txt', 'r')
        lap_times = laptimes.readlines()
        lap_times = [x.strip() for x in lap_times]
        print(lap_times)
        lines = len(lap_times)
        if lines < i+1:
            laptimes = open('laptimes.txt', 'a')
            laptimes.write("DNF DNF DNF\n")

    data = open('laptimes.txt', 'r')
    data_lines = data.readlines()
    data_lines = [x.strip() for x in data_lines]
    fitnesses = []
    for line in data_lines:
        if line == "DNF DNF DNF":
            fitnesses.append(1000)
        else:
            data_points = line.split(' ')
            fitness = float(data_points[0])+10*float(data_points[1])+float(data_points[2])
            fitnesses.append(fitness)
    print(fitnesses)
    fastest_idx = np.argmin(fitnesses)

    evolution_fitness = open('fitnesses.txt', 'a')
    evolution_fitness.write(str(track_id) + ' ' + str(min(fitnesses))+'\n')

    print("The fastest child was number: ", fastest_idx)
    filename = 'EVO'+str(fastest_idx)+'.h5'
    os.remove(os.path.join('Best_Model.h5'))
    shutil.copy(os.path.join(loc, filename), os.path.join('Best_Model.h5'))
    noise *= 0.9
    make_childs_new(best_model, population, loc, noise)
    open('laptimes.txt', 'w') #delete results for new generation
