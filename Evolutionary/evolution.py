import shutil
import os
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

while True:
    for i in range(population):
        filename = 'EVO'+str(i)+'.h5'
        shutil.copy(os.path.join(loc, filename), os.path.join('EVO_model.h5'))

    laptimes = open('laptimes.txt', 'r')
    lap_times = laptimes.readlines()
    lap_times = [float(x.strip()) for x in lap_times]
    max_lap = max(lap_times)
    min_lap = min(lap_times)
    fitness = [(x-min(lap_times))/(max(lap_times)-min(lap_times)) for x in lap_times] #scale from 0 to 1
    fitness = [x/sum(fitness) for x in fitness] #normalize total to sum to 1.
    make_new_parent(fitness, loc, population)
