from pytocl.driver import Driver
import time
from pytocl.car import State, Command
import numpy as np
from nn import predict_output, load_keras_model

class MyDriver(Driver):
	def __init__(self):
		name = 'Best_Model.h5'
		self.model = load_keras_model(name)
		self.time_offset = 0
		self.population = 10
		self.time = 0
		self.laptimes = np.zeros(self.population)
		self.child = 0
		self.been_outside_track = False
		self.time_outside_circuit = 0
		self.start_time = None

	def drive(self, carstate: State) -> Command:
		data = []
		command = Command()
		angle = carstate.angle
		speed = carstate.speed_x
		track_position = carstate.distance_from_center
		track_edges = carstate.distances_from_edge
		data.append(speed)
		data.append(track_position)
		data.append(angle)

		for i in track_edges:
			data.append(i)
		command.accelerator, command.brake, command.steering = predict_output(self.model, data)
		if carstate.rpm > 8000:
			command.gear = carstate.gear + 1
		elif carstate.rpm < 3000 and carstate.gear > 1:
			command.gear = carstate.gear - 1
		if not command.gear:
			command.gear = carstate.gear or 1

		if sum (track_edges) < 0 and not self.been_outside_track:
			self.start_time = time.time()
			self.been_outside_track = True
			#print ('Ive been outside the track')

		if sum (track_edges) > 0 and self.been_outside_track:
			end_time = time.time()
			self.time_outside_circuit += end_time - self.start_time
			#print ('Im in the track again, and was out for',end_time - self.start_time)
			#print ('Total time out is',self.time_outside_circuit)
			self.been_outside_track = False

		if carstate.last_lap_time != self.time:
			self.time = carstate.last_lap_time
			fitness = carstate.last_lap_time
			fitnesses = open('laptimes.txt', 'a')
			#fitnesses.write("%s \n" %fitness)
			fitnesses.write(str(fitness) + ' ' + str(self.time_outside_circuit) + ' ' +str(carstate.damage) + '\n')
		#if carstate.current_lap_time > 10 and carstate.distance_from_start < 10:
			#exit()
		return command