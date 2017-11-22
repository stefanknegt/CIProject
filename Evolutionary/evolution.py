import shutil
import os
import wrapper
import time
from evolution_nn import load_keras_model, get_weights, make_childs, make_new_parent
population = 10
start_model = 'Best_Model.h5'
loc = 'EVO_models'

if __name__ == "__main__":
    if not os.path.exists(loc):
        os.makedirs(loc)
    new_model = load_keras_model(start_model)
    w,b = get_weights(new_model)
    make_childs(w, b, loc, population)
    open('laptimes.txt', 'w') #delete old results

while True:
    for i in range(population):
        filename = 'EVO'+str(i)+'.h5'
        shutil.copy(os.path.join(loc, filename), os.path.join('EVO_model.h5'))
        trained_once = wrapper.train_once()
        time.sleep(20)
        print ('trained',filename)
        os.remove(os.path.join('EVO_model.h5'))
        #check if laptime was registered else DNF
        
        laptimes = open('laptimes.txt', 'r')
        lap_times = laptimes.readlines()
        lap_times = [x.strip() for x in lap_times]
        print(lap_times)
        lines = len(lap_times)
        print("The amount of lap_times: ",lines)
        if lines < i+1:
            laptimes = open('laptimes.txt', 'a')
            laptimes.write("DNF \n")

    laptimes = open('laptimes.txt', 'r')
    lap_times = laptimes.readlines()
    lap_times = [x.strip() for x in lap_times]
    lap_times = [0 if x == "DNF" else float(x) for x in lap_times]
    lap_times = [max(lap_times) if x==0 else x for x in lap_times]
    if min(lap_times) != max(lap_times):
    	fitness = [max(lap_times)-x for x in lap_times] #fastest lap gets highest value
    else:
        fitness = lap_times #this only occurs when all lap_times are the same...
    fitness = [x/sum(fitness) for x in fitness] #normalize total to sum to 1.
    print(fitness)
    make_new_parent(fitness, loc, population)
    open('laptimes.txt', 'w') #delete results for new generation
