"""
Created on Tue Jul 24 09:05:15 2018

@author: agrah
"""
import math

from ThesisImplementation.DriverModel import DriverModel
# import DrivingLogic
import sys
import ThesisImplementation.constant as constant
import json
from ThesisImplementation.neighbour import GetNeighbour


def dist(x1, y1, x2, y2):
    return math.sqrt(
        abs(pow(x1 - x2, 2)) + abs(pow(y1 - y2, 2)))


class vehicle:

    def __init__(self, type, canvas, lane, offset, ids):

        self.type = type
        self.id = ids
        self.color = None
        self.dimension = None
        self.new_vehicle = None
        self.canvas = canvas
        self.lane = lane
        self.control = DriverModel()

        if type not in constant.vehicle_type:
            print("invalid vehicle type, cannot create new vehicle")
            sys.exit()
        else:
            with open("vehicle_dimension.json") as f:
                vehicles = json.load(f)["vehicle"]
            for vehicle in vehicles:
                if vehicle["type"] == self.type:
                    self.color = vehicle["color"]
                    self.dimension = vehicle["dimension"]
            padding = 5
            other_lane = 35
            if lane == 1:
                self.new_vehicle = self.canvas.create_rectangle(0 + offset, 0, self.dimension[0] + offset,
                                                                self.dimension[1],
                                                                fill=self.color)
            else:
                self.new_vehicle = self.canvas.create_rectangle(0 + offset, 0 + other_lane, self.dimension[0] +
                                                                offset, self.dimension[1] + other_lane,
                                                                fill=self.color)
            self.control.position = self.canvas.coords(self.new_vehicle)
            self.control.speed = [0.5, 0]
            self.control.lane = self.lane
            # print(self.control.self_obj)

    def __str__(self):
        return "vehicle: " + str(self.id)

    def DrivingLogic(self, vehicle_info):
        acc = vehicle_info[0]
        ret = vehicle_info[1]
        speed = vehicle_info[2]
        own_pos = vehicle_info[3]
        own_lane = vehicle_info[4]
        dir = vehicle_info[5]
        request = vehicle_info[7]
        flag = vehicle_info[8]
        nei = GetNeighbour().update_neighbour(self)
        max_speed = []
        min_speed = []
        min_retardation = 15
        max_retardation = 15
        min_acceleration = 2
        max_acceleration = 50

        d_car = 20
        d_bus = 40
        d_critical = 15
        # own_pos = self.control.position
        # own_lane = self.control.lane
        # print("()()()()()()(()()()()()))()(()())())())()(",self,own_lane)
        if self.type == 'bus':
            if own_pos[0] >= 300:
                speed[0] = speed[0] - (speed[0] * max_retardation) / 100
        elif flag:
            if request[2] != 0:
                speed[0] = request[0]
                request[3] = request[3] - speed[0]
                print("-------", request[1], self, "iteration", request[2])
                reduced_speed = speed[0] - request[1]
                request[0] = reduced_speed
                request[2] = request[2] - 1
            else:
                if request[3] > 0:
                    speed[0] = request[0]
                    request[3] = request[3] - speed[0]
                else:
                    if request[4] == self:
                        # speed[0] = request[0]
                        if not own_pos[1] <= 0:
                            if request[6] == 1:
                                speed[1] = -0.3
                                speed[0] = 0.3
                            elif request[6] == 2:
                                if request[7]:
                                    speed[1] = -0.3
                                    speed[0] = 0.3
                                elif request[8]:
                                    speed[1] = -0.3
                                    speed[0] = 0.3
                                elif request[5] is not None:
                                    speed[1] = -0.5
                                    speed[0] = 0.5
                                else:
                                    speed[1] = -0.5
                                    speed[0] = 0.5
                            else:
                                if request[7]:
                                    speed[1] = -0.3
                                    speed[0] = 0.3
                                else:
                                    speed[1] = -0.4
                                    speed[0] = 0.4

                        else:

                            speed[1] = 0
                            speed[0] = 0.4

                            self.control.request = []
                            self.control.flag = False
                            print("---------------Hi I am done with the lane change *+*+*+*++*+*+*+*+*+*+*+*+*+*+*",
                                  self, " ", self.control.lane, "+++++++++++++++++++++++++++++++++++++++++++++++"
                                                                "++++++++++++++")
                            if request[5] is not None:
                                request[5].control.request = []
                                request[5].control.flag = False
                                # request[5].control.speed[0] = 0.5
        else:
            if len(nei) != 0:
                vehicle_in_front_check = False
                vehicle_in_back = False
                vehicle_in_front = False
                for veh in nei:
                    nei_pos = veh.control.position
                    nei_lane = veh.control.lane
                    distance = dist(own_pos[2], (own_pos[1] + own_pos[3]) / 2, nei_pos[0], (nei_pos[3] + nei_pos[1]) / 2)
                    # print(self, " in lane ", own_lane, " computing distance with ", veh, "which is in lane ", nei_lane,
                    #       " with distance ", distance)
                    if own_pos[2] < nei_pos[0] and distance < 30 and veh.type is not 'bus':
                        vehicle_in_front = True
                    if nei_lane == own_lane:
                        print(self, " in lane ", own_lane, " computing distance with ", veh, "which is in lane ", nei_lane,
                              " with distance ", distance)
                        if veh.type == 'car':
                            if own_pos[2] < nei_pos[0]:
                                vehicle_in_front_check = True
                                if distance == d_car:
                                    speed[0] = speed[0]
                                elif distance < d_car:
                                    if distance < d_critical:
                                        print("distance less than critical, reducing speed")
                                        speed[0] = speed[0] - (speed[0] * min_retardation) / 100
                                    else:
                                        print("distance less than safe, reducing speed")
                                        speed[0] = speed[0] - (speed[0] * min_retardation) / 100
                                elif distance > d_car:
                                    if speed[0] < 0.5:
                                        print("distance more than safe, increasing speed")
                                        speed[0] = speed[0] + (speed[0] * min_acceleration) / 100
                            elif own_pos[2] > nei_pos[0]:
                                vehicle_in_back = True

                        elif veh.type == 'bus':
                            if own_pos[2] < nei_pos[0]:
                                vehicle_in_front_check = True
                                if distance < d_bus:
                                    if distance < d_critical:
                                        speed[0] = speed[0] - (speed[0] * max_retardation) / 100
                                    else:
                                        previous_vehicle = None
                                        parallel_vehicle = None
                                        for i in nei:
                                            temp_lane = i.control.lane
                                            temp_pos = i.control.position
                                            if temp_lane != own_lane:

                                                if own_pos[0] > temp_pos[2]:
                                                    previous_vehicle = i
                                                    print("previous vehicle: ", previous_vehicle)
                                                elif own_pos[0] <= temp_pos[0] or own_pos[0] > temp_pos[0]:
                                                    print(temp_pos[0] - own_pos[0],i, "++++", temp_pos)
                                                    print("parallel vehicle: ", parallel_vehicle)
                                                    if abs(own_pos[0] - temp_pos[0]) < 5:
                                                        parallel_vehicle = i
                                            else:
                                                if own_pos[0] > temp_pos[2]:
                                                    vehicle_in_back = True

                                        # -----the calculation is based on equation of motions
                                        # -----v = u + at
                                        # -----s = ut + 1/2at^2
                                        if veh.control.speed[0] is not 0:
                                            bus_retardation = (veh.control.speed[0] * min_retardation) / 100
                                            d_stop_time = veh.control.speed[0] / bus_retardation
                                            d_stop = (veh.control.speed[0] * d_stop_time - 1 / 2 * (bus_retardation *
                                                                                                pow(d_stop_time, 2)))
                                        else:
                                            d_stop_time = 0
                                            d_stop = 0
                                        delta_d1 = d_bus - d_critical
                                        if previous_vehicle is not None and parallel_vehicle is not None:
                                            print("---------------------------triggering case 1----------------------\
                                            -----")
                                            time = (d_car + d_stop + delta_d1) / parallel_vehicle.control.speed[0]
                                            distance_by_potential_car = d_stop + delta_d1
                                            reduced_speed_potential_car = distance_by_potential_car / time
                                            ret = abs((speed[0] - reduced_speed_potential_car) / d_stop_time)
                                            self.control.retardation = ret
                                            speed[0] = speed[0] - ret
                                            self.control.requestedSpeed = [speed[0], ret, round(d_stop_time),
                                                                           distance_by_potential_car, self,
                                                                           previous_vehicle, 1, vehicle_in_back,
                                                                           vehicle_in_front]
                                            delta_d2 = math.sqrt(pow(d_critical, 2) + pow(35, 2))
                                            distance_by_previous_car = delta_d2 - delta_d1 - d_stop
                                            reduced_speed_previous_vehicle = (delta_d2 - delta_d1 - d_stop) / time
                                            retardation_previous_vehicle = (previous_vehicle.control.
                                                                            speed[0] - reduced_speed_previous_vehicle)\
                                                                             / d_stop_time
                                            previous_vehicle.control.requestedSpeed = [
                                                previous_vehicle.control.speed[0]-retardation_previous_vehicle,
                                                retardation_previous_vehicle,
                                                round(d_stop_time), distance_by_previous_car, self, previous_vehicle, 1,
                                                vehicle_in_back, vehicle_in_front]

                                            self.control.flag = True
                                            previous_vehicle.control.flag = True
                                        elif previous_vehicle is None and parallel_vehicle is None or previous_vehicle \
                                                is not None and parallel_vehicle is None:
                                            print("---------------------------triggering case 2----------------------"
                                                  "-----")
                                            self.control.requestedSpeed = [speed[0],
                                                                           0,
                                                                           0,
                                                                           0,
                                                                           self,
                                                                           previous_vehicle,
                                                                           2,
                                                                           vehicle_in_back,
                                                                           vehicle_in_front]
                                            self.control.flag = True
                                        elif previous_vehicle is None and parallel_vehicle is not None:
                                            print("---------------------------triggering case 3-----------------------"
                                                  "----")
                                            time = (d_car + d_stop + delta_d1) / parallel_vehicle.control.speed[0]
                                            distance_by_potential_car = d_stop + delta_d1
                                            reduced_speed_potential_car = distance_by_potential_car / time
                                            ret = abs((speed[0] - reduced_speed_potential_car) / d_stop_time)
                                            self.control.retardation = ret
                                            speed[0] = speed[0] - ret
                                            self.control.requestedSpeed = [speed[0],
                                                                           ret,
                                                                           round(d_stop_time),
                                                                           distance_by_potential_car,
                                                                           self,
                                                                           previous_vehicle,
                                                                           3,
                                                                           vehicle_in_back,
                                                                           vehicle_in_front]
                                            self.control.flag = True

                                elif distance > d_bus:
                                    speed[0] = speed[0] + (speed[0] * min_acceleration) / 100

                if not vehicle_in_front_check:
                    if self.id is not 3:
                        if not speed[0] > 0.5:
                            speed[0] = speed[0] + (speed[0] * min_acceleration) / 100
                    else:
                        speed[0] = 0.5

            else:
                print("===================", self, " have no neighbour========================")
                if self.id is not 3:
                    if not speed[0] > 0.5:
                        speed[0] = speed[0] + (speed[0] * min_acceleration) / 100
                else:
                    speed[0] = 0.5

        if speed[0] < 0.01:

            if self.type is not 'bus':
                speed[0] = 0.01
            else:
                speed[0] = 0

        return speed

    def move(self):

        info = self.control.vehicle_info
        speed = self.DrivingLogic(info)
        print(speed, self)
        self.canvas.move(self.new_vehicle, speed[0], speed[1])
        pos = self.canvas.coords(self.new_vehicle)
        print(self, pos, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if pos[1] < 18:
            updated_lane = 1
        else:
            updated_lane = 2
        self.update_value({'speed': speed, 'position': pos, 'lane': updated_lane})
        return speed

    def update_value(self, vehicle_info):
        nei = GetNeighbour()
        driver_model = self.control
        driver_model.speed = vehicle_info.get('speed')
        driver_model.position = vehicle_info.get('position')
        driver_model.lane = vehicle_info.get('lane')
        driver_model.neighbour_info = nei.update_neighbour(self)
        # print(driver_model.neighbour_info)
