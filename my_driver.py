from pytocl.driver import Driver
from pytocl.car import State, Command
import numpy as np
from nn_all import predict_output, load_keras_model

class MyDriver(Driver):
	def __init__(self):
		self.model = load_keras_model('LSTM_NotSpring.h5')
	def drive(self, carstate: State) -> Command:
		nn_type = "LSTM"
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
		print(data)
		command.accelerator, command.brake, command.steering = predict_output(self.model, data, nn_type)		
		if carstate.rpm > 5000:
			command.gear = carstate.gear + 1
		elif carstate.rpm < 2500:
			command.gear = carstate.gear - 1
		if not command.gear:
			command.gear = carstate.gear or 1
		return command
