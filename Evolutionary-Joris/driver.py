import logging
import csv
import math
import numpy as np
from pytocl.analysis import DataLogWriter
from pytocl.car import State, Command, MPS_PER_KMH
from pytocl.controller import CompositeController, ProportionalController, \
    IntegrationController, DerivativeController

_logger = logging.getLogger(__name__)

class Driver:
    """
    Driving logic.

    Implement the driving intelligence in this class by processing the current
    car state as inputs creating car control commands as a response. The
    ``drive`` function is called periodically every 20ms and must return a
    command within 10ms wall time.
    """

    def __init__(self, logdata=False):
        self.steering_ctrl = CompositeController(
            ProportionalController(0.4),
            IntegrationController(0.2, integral_limit=1.5),
            DerivativeController(2)
        )
        self.acceleration_ctrl = CompositeController(
            ProportionalController(3.7),
        )
        self.data_logger = DataLogWriter() if logdata else None

        self.train_data = []
        self.written = False


    @property
    def range_finder_angles(self):
        """Iterable of 19 fixed range finder directions [deg].

        The values are used once at startup of the client to set the directions
        of range finders. During regular execution, a 19-valued vector of track
        distances in these directions is returned in ``state.State.tracks``.
        """
        return -90, -75, -60, -45, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, \
            30, 45, 60, 75, 90

    def on_shutdown(self):
        """
        Server requested driver shutdown.

        Optionally implement this event handler to clean up or write data
        before the application is stopped.
        """
        if self.data_logger:
            self.data_logger.close()
            self.data_logger = None

    def drive(self, carstate: State) -> Command:
        """
        Produces driving command in response to newly received car state.

        This is a dummy driving routine, very dumb and not really considering a
        lot of inputs. But it will get the car (if not disturbed by other
        drivers) successfully driven along the race track.
        """
        command = Command()
        self.steer(carstate, 0.0, command)

        # ACC_LATERAL_MAX = 6400 * 5
        # v_x = min(80, math.sqrt(ACC_LATERAL_MAX / abs(command.steering)))
        v_x = max(50,max(carstate.distances_from_edge))

        if v_x == 200.0:
            v_x = 500.0

        if (carstate.speed_x*3.6 - v_x > 0 ):
            diff = carstate.speed_x*3.6 - v_x
            command.brake = 1.1 / (1 + np.exp(-1*(diff-20)))
        # print ('braking is',command.brake)

        self.accelerate(carstate, v_x, command)
        #self.data_logger.log(carstate, command)
        data = []
        data.append(command.accelerator)
        data.append(command.brake)
        data.append(command.steering)
        data.append(carstate.speed_x)
        data.append(carstate.speed_y) # NEW
        data.append(carstate.speed_z) # NEW

        data.append(carstate.distance_from_center)
        data.append(carstate.angle)

        for i in carstate.wheel_velocities:
            data.append(i)

        for i in carstate.distances_from_edge:
            data.append(i)

        self.train_data.append(data)
        # a.writerow(data)

        if carstate.last_lap_time > 0.0 and not self.written:
            b = open('Joris-Data/Wheel2.csv', 'w')
            a = csv.writer(b)
            a.writerows(self.train_data)
            b.close()
            print ('Rondje gereden')
            self.written = True

        return command

    def accelerate(self, carstate, target_speed, command):
        # compensate engine deceleration, but invisible to controller to
        # prevent braking:
        speed_error = 1.0025 * target_speed * MPS_PER_KMH - carstate.speed_x
        acceleration = self.acceleration_ctrl.control(
            speed_error,
            carstate.current_lap_time
        )

        # stabilize use of gas and brake:
        acceleration = math.pow(acceleration, 3)

        if acceleration > 0:
            if abs(carstate.distance_from_center) >= 1:
                # off track, reduced grip:
                acceleration = min(0.4, acceleration)

            command.accelerator = min(acceleration, 1)

            if carstate.rpm > 8000:
                command.gear = carstate.gear + 1

        # else:
        #     command.brake = min(-acceleration, 1)

        if carstate.rpm < 3500:
            command.gear = carstate.gear - 1

        if not command.gear:
            command.gear = carstate.gear or 1

    def steer(self, carstate, target_track_pos, command):
        steering_error = target_track_pos - carstate.distance_from_center

        for i in range(0,len(carstate.opponents)):
            if carstate.opponents[i] < 7.0:
                #print ('Opponent detected at',-180.0 + i*10,'degrees')
                if i==4 or i==5 or i==6 or i==7 or i==8 or i==9:
                    steering_error += -1
                    #print ('Steering to the right')
                if i==27 or i==28 or i==29 or i==30 or i==31 or i==32:
                    #command.steering == 1.0
                    #print ('Steering to the left')
                    steering_error += 1

        if carstate.speed_x > 120/3.6:
            command.steering = 0.1 * self.steering_ctrl.control(
                steering_error,
                carstate.current_lap_time)
        elif carstate.speed_x > 100/3.6:
            command.steering = 0.2 * self.steering_ctrl.control(
                steering_error,
                carstate.current_lap_time)
        elif carstate.speed_x > 80/3.6:
            command.steering = 0.25 * self.steering_ctrl.control(
                steering_error,
                carstate.current_lap_time)
        elif carstate.speed_x > 70/3.6:
            command.steering = 0.3 * self.steering_ctrl.control(
                steering_error,
                carstate.current_lap_time)
        else:
            command.steering = self.steering_ctrl.control(
                steering_error,
                carstate.current_lap_time)
            #print ('Steering is',command.steering)


