from pytocl.driver import Driver
from pytocl.car import State, Command
import numpy as np
from nn import predict_output, load_keras_model

class MyDriver(Driver):
	def __init__(self):
		name = 'EVO_model.h5'
		self.model = load_keras_model(name)
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
		if carstate.rpm > 5000:
			command.gear = carstate.gear + 1
		elif carstate.rpm < 2500 and carstate.gear > 1:
			command.gear = carstate.gear - 1
		if not command.gear:
			command.gear = carstate.gear or 1

		return command
