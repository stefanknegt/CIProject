from pytocl.driver import Driver
from pytocl.car import State, Command
import numpy as np
from nn import predict_output, load_keras_model
#from evolution_nn import make_new_parent
from subprocess import call


class MyDriver(Driver):
	def __init__(self):
		name = 'MLPLALL4.h5'
		self.model = load_keras_model(name)
		self.time_offset = 0
		self.population = 10
		self.time = 0
		self.laptimes = np.zeros(self.population)
		self.child = 0
	def drive(self, carstate: State) -> Command:		
		data = []
		command = Command()
		angle = carstate.angle #ANGLE_TO_TRACK_AXIS
		speed = carstate.speed_x #SPEED
		track_position = carstate.distance_from_center #Track position
		track_edges = carstate.distances_from_edge #TRACK_EDGE0-18
		data.append(speed)
		data.append(track_position)
		data.append(angle)
		for i in track_edges:
			data.append(i)
		command.accelerator, command.brake, command.steering = predict_output(self.model, data)
		if carstate.rpm > 5000:
			command.gear = carstate.gear + 1
		elif carstate.rpm < 2500 and carstate.gear > 1:
			command.gear = carstate.gear - 1
		if not command.gear:
			command.gear = carstate.gear or 1

		if carstate.last_lap_time != 0:
			fitness = carstate.last_lap_time
			print(fitness)
			call(['bash', './start.sh'])
			exit()

		return command
