# from .vehicleGenerator import vehicleGenerator
import math


def singleton(myClass):
    _instances = {}

    def getInstances(*args, **kwargs):
        if myClass not in _instances:
            _instances[myClass] = myClass(*args, **kwargs)
        return _instances[myClass]
    return getInstances


@singleton
class GetNeighbour:

    def __init__(self, list=[]):

        self.vehicle_list = list
        # print(self.vehicle_list)
        self.neighbour = {}
        self.neighbour_range = 55
        self.neighbour_bus_range = 65
        self.report_dict = {}
        for v in self.vehicle_list:
            self.neighbour[v] = []
            self.report_dict[v] = []

    def update_neighbour(self, own_vehicle):

        own_vehicle_control = own_vehicle.control
        own_position = mean(own_vehicle_control.position[0], own_vehicle_control.position[1],
                            own_vehicle_control.position[2], own_vehicle_control.position[3])
        neighbour_list = self.neighbour.get(own_vehicle)

        for vehicle in self.vehicle_list:
            if vehicle is not own_vehicle:
                control = vehicle.control
                position = mean(control.position[0], control.position[1],
                                control.position[2], control.position[3])
                distance = dist(position[0], position[1], own_position[0], own_position[1])

                if vehicle.type == 'bus':
                    if distance <= self.neighbour_bus_range:
                        # print(own_vehicle, " has neighbour ", vehicle, " with distance ", distance)
                        if vehicle not in neighbour_list:
                            neighbour_list.append(vehicle)
                    else:
                        if vehicle in neighbour_list:
                            neighbour_list.remove(vehicle)
                else:
                    if distance <= self.neighbour_range:
                        # print(own_vehicle, " has neighbour ", vehicle, " with distance ", distance)
                        if vehicle not in neighbour_list:
                            neighbour_list.append(vehicle)
                    else:
                        if vehicle in neighbour_list:
                            neighbour_list.remove(vehicle)

        return neighbour_list

    def report(self, vehicle, speed):

        speed_list = self.report_dict[vehicle]
        s = math.sqrt(abs(pow(speed[0], 2)) + abs(pow(speed[1], 2)))
        speed_list.append(s)

    def avg_speed_report(self, vehicle, speed):

        speed_list = self.report_dict[vehicle]
        s = math.sqrt(abs(pow(speed[0], 2)) + abs(pow(speed[1], 2)))
        if len(speed_list) is not 0:
            speed_list[0] = (speed_list[0]+s)/2
        else:
            speed_list.append(s)

    def distance_report(self, vehicle, distance):
        dist_list = self.report_dict[vehicle]
        dist_list.append(distance)

    def print_report(self, vehicle):

        print(vehicle, ":", self.report_dict[vehicle])
        # print(vehicle, ":", self.report_dict)


def dist(x1, y1, x2, y2):
    return math.sqrt(
        abs(pow(x1 - x2, 2)) + abs(pow(y1 - y2, 2)))


def mean(x1, y1, x2, y2):
    return [(x1 + x2) / 2, (y1 + y2) / 2]





