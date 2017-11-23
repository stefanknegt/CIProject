import shutil
import os
import wrapper
import time
from evolution_nn import make_childs_new, make_new_parent
import numpy as np
population = 5
best_model = 'Best_Model.h5'
loc = 'EVO_models'

if __name__ == "__main__":
    if not os.path.exists(loc):
        os.makedirs(loc)
    make_childs_new(best_model, population, loc)
    open('laptimes.txt', 'w') #delete old results

while True:
    for i in range(population):
        filename = 'EVO'+str(i)+'.h5'
        shutil.copy(os.path.join(loc, filename), os.path.join('EVO_model.h5'))
        trained_once = wrapper.train_once()
        time.sleep(15)
        print ('trained',filename)
        os.remove(os.path.join('EVO_model.h5'))
        #check if laptime was registered else DNF
        
        laptimes = open('laptimes.txt', 'r')
        lap_times = laptimes.readlines()
        lap_times = [x.strip() for x in lap_times]
        print(lap_times)
        lines = len(lap_times)
        if lines < i+1:
            laptimes = open('laptimes.txt', 'a')
            laptimes.write("DNF \n")

    laptimes = open('laptimes.txt', 'r')
    lap_times = laptimes.readlines()
    lap_times = [x.strip() for x in lap_times]
    lap_times = [0 if x == "DNF" else float(x) for x in lap_times]
    lap_times = [max(lap_times) if x==0 else x for x in lap_times]
    fastest_idx = np.argmin(lap_times)
    print("The fastest child was number: ", fastest_idx)
    filename = 'EVO'+str(fastest_idx)+'.h5'
    os.remove(os.path.join('Best_Model.h5'))
    shutil.copy(os.path.join(loc, filename), os.path.join('Best_Model.h5'))
    make_childs_new(best_model, population, loc)
    open('laptimes.txt', 'w') #delete results for new generation

    '''
    if min(lap_times) != max(lap_times):
    	fitness = [max(lap_times)-x for x in lap_times] #fastest lap gets highest value
    else:
        fitness = lap_times #this only occurs when all lap_times are the same...
    fitness = [x/sum(fitness) for x in fitness] #normalize total to sum to 1.
    print(fitness)
    make_new_parent(fitness, loc, population)
    '''
