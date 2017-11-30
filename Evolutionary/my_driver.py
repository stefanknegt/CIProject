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
		self.time = 0
		self.been_outside_track = False
		self.time_outside_circuit = 0
		self.start_time = None
	def drive(self, carstate: State) -> Command:
		data = []
		command = Command()
		angle = carstate.angle
		speed_x = carstate.speed_x
		#speed_y = carstate.speed_y
		#speed_z = carstate.speed_z
		track_position = carstate.distance_from_center
		track_edges = carstate.distances_from_edge
		#wheel_velocities = carstate.wheel_velocities
		data.append(speed_x)
		data.append(track_position)
		data.append(angle)

		for i in track_edges:
			data.append(i)
		out, command.steering = predict_output(self.model, data)
		if out > 0:
			command.accelerator = out
			command.brake = 0
		elif out <= 0:
			command.accelerator = 0
			command.brake = -out
		if carstate.rpm > 5000:
			command.gear = carstate.gear + 1
		elif carstate.rpm < 2500 and carstate.gear > 1:
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
			print ('Im in the track again, and was out for',end_time - self.start_time)
			print ('Total time out is',self.time_outside_circuit)
			self.been_outside_track = False

		if carstate.last_lap_time != self.time:
			self.time = carstate.last_lap_time
			fitness = carstate.last_lap_time
			fitnesses = open('laptimes.txt', 'a')
			fitnesses.write(str(fitness) + ' ' + str(self.time_outside_circuit) + ' ' +str(carstate.damage) + '\n')

		return command
