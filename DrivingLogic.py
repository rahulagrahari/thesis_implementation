
def DrivingLogic(vehicle_info):

    acc = vehicle_info[0]
    ret = vehicle_info[1]
    speed = vehicle_info[2]
    pos = vehicle_info[3]
    lane = vehicle_info[4]
    dir = vehicle_info[5]
    request = vehicle_info[7]
    flag = vehicle_info[8]
    nei = GetNeighbour().update_neighbour(self)
    max_speed = []
    min_speed = []
    min_retardation = 15
    max_retardation = 50
    min_acceleration = 20
    max_acceleration = 50

    d_car = 20
    d_bus = 40
    d_critical = 15
    own_pos = self.control.position
    own_lane = self.control.lane
    # print(nei)
    if self.type == 'bus':
        if own_pos[0] >= 300:
            speed[0] = speed[0] - (speed[0] * min_retardation) / 100
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
                    speed[0] = request[0]
                    if not own_pos[1] <= 0:
                        speed[1] = -0.5
                    else:
                        speed[1] = 0
                        print("---------------Hi I am done with the lane change --------------")
                        self.control.request = []
                        self.control.flag = False
                        request[5].control.request = []
                        request[5].control.flag = False
                        request[5].control.speed[0] = 0.5
    else:
        for veh in nei:
            nei_pos = veh.control.position
            nei_lane = veh.control.lane
            distance = dist(own_pos[2], (own_pos[1] + own_pos[3]) / 2, nei_pos[0], (nei_pos[3] + nei_pos[1]) / 2)
            # print(self, " in lane ", own_lane, " computing distance with ", veh, "which is in lane ", nei_lane,
            #       " with distance ", distance)
            if nei_lane == own_lane:
                if veh.type == 'car':
                    if own_pos[2] < nei_pos[0]:
                        if distance < d_car:
                            if distance < d_critical:
                                speed[0] = speed[0] - (speed[0] * max_retardation) / 100
                            else:
                                speed[0] = speed[0] - (speed[0] * min_retardation) / 100
                        elif distance > d_car:
                            speed[0] = speed[0] + (speed[0] * min_acceleration) / 100
                elif veh.type == 'bus':
                    if own_pos[2] < nei_pos[0]:
                        if distance < d_bus:
                            if distance < d_critical:
                                speed[0] = speed[0] - (speed[0] * max_retardation) / 100
                            else:
                                for i in nei:
                                    temp_lane = i.control.lane
                                    if temp_lane != own_lane:
                                        temp_pos = i.control.position
                                        if own_pos[0] > temp_pos[2]:
                                            previous_vehicle = i
                                            print("previous vehicle: ", previous_vehicle)
                                        elif own_pos[0] <= temp_pos[0]:
                                            parallel_vehicle = i
                                            print("parallel vehicle: ", parallel_vehicle)
                                # -----the calculation is based on equation of motions
                                # -----v = u + at
                                # -----s = ut + 1/2at^2
                                bus_retardation = (veh.control.speed[0] * min_retardation) / 100
                                d_stop_time = veh.control.speed[0] / bus_retardation
                                d_stop = (veh.control.speed[0] * d_stop_time - 1 / 2 * (bus_retardation *
                                                                                        pow(d_stop_time, 2)))
                                delta_d1 = d_bus - d_critical
                                time = (d_car + d_stop + delta_d1) / parallel_vehicle.control.speed[0]
                                distance_by_potential_car = d_stop + delta_d1
                                reduced_speed_potential_car = distance_by_potential_car / time
                                ret = abs((speed[0] - reduced_speed_potential_car) / d_stop_time)
                                self.control.retardation = ret
                                speed[0] = speed[0] - ret
                                self.control.requestedSpeed = [speed[0], ret, round(d_stop_time),
                                                               distance_by_potential_car, self, previous_vehicle]
                                delta_d2 = math.sqrt(pow(d_critical, 2) + pow(35, 2))
                                distance_by_previous_car = delta_d2 - delta_d1 - d_stop
                                reduced_speed_previous_vehicle = (delta_d2 - delta_d1 - d_stop) / time
                                retardation_previous_vehicle = (previous_vehicle.control.
                                                                speed[0] - reduced_speed_previous_vehicle) / \
                                                               d_stop_time
                                previous_vehicle.control.requestedSpeed = [
                                    previous_vehicle.control.speed[0] - retardation_previous_vehicle,
                                    retardation_previous_vehicle,
                                    round(d_stop_time), distance_by_previous_car, self, previous_vehicle]

                                self.control.flag = True
                                previous_vehicle.control.flag = True

                        elif distance > d_bus:
                            speed[0] = speed[0] + (speed[0] * min_acceleration) / 100

    if speed[0] < 0.01:
        speed[0] = 0

    return speed
