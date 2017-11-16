from pytocl.main import main
from my_driver_evo import MyDriver
import numpy as np
from evolution_nn import

def calculate_fitness():
    population = 100
    except:
        laptimes = np.load('laptimes.npy')
    as:
        print("Making a new laptime matrix")
        laptimes = np.zeros(population)
        np.save('laptimes.npy', laptimes)
    for i in range(0,population):
        main(MyDriver(i))

def generate_children():
    laptimes = np.load('laptimes.npy')
    fitness = 
