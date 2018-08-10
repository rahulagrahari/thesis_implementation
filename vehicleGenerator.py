# import random
# from random import shuffle
from ThesisImplementation.vehicle import vehicle
from ThesisImplementation.neighbour import GetNeighbour
from win32api import GetSystemMetrics

class vehicleGenerator:

    def __init__(self, canvas, case=0):

        self.vehicle_list = []
        self.car_list = []
        self.bus_list = []
        self.canvas = canvas
        # car01 = vehicle('car', canvas, 1, -280, 1)
        # car02 = vehicle('car', canvas, 1, -240, 1)
        # car03 = vehicle('car', canvas, 1, -200, 1)
        # car04 = vehicle('car', canvas, 1, -160, 1)
        # car05 = vehicle('car', canvas, 1, -120, 1)
        # car06 = vehicle('car', canvas, 1, -80, 1)
        # car07 = vehicle('car', canvas, 1, -40, 1)

        # car1 = vehicle('car', canvas, 1, 0, 1)
        # car2 = vehicle('car', canvas, 1, 40, 2)
        # car3 = vehicle('car', canvas, 1, 80, 3)
        # car4 = vehicle('car', canvas, 2, 0, 4)
        # car5 = vehicle('car', canvas, 2, 40, 5)
        # bus = vehicle('bus', canvas, 2, 100, 6)

        # canvas.create_rectangle(101.66, 35, 101.66, 45, fill='green')
        canvas.create_rectangle(301.66, 35, 301.66, 45, fill='green')
        canvas.create_rectangle(0, 1, GetSystemMetrics(0), 1, fill='black')
        canvas.create_rectangle(0, 50, GetSystemMetrics(0), 50, fill='black')
        gap = 5
        x1 = 0
        x2 = 5
        y = 23
        for i in range(1, 100):

            canvas.create_rectangle(x1, y, x2, y, fill='black')
            x1 = x1 + 5*gap
            x2 = x2 + 5*gap

        # v_list = [car1, car2, car3, car4, car5, bus]
        # g = GetNeighbour(v_list)
        # self.vehicle_list = v_list

        if case == 0:
            self.parallel_missing_previous_available()
        elif case == 1:
            self.parallel_available_previous_missing()
        elif case == 2:
            self.parallel_and_previous_car_available()
        elif case == 3:
            self.parallel_and_previous_missing()
        else:
            print("wrong output")

    def parallel_and_previous_car_available(self):

        car1 = vehicle('car', self.canvas, 1, 0, 1)
        car2 = vehicle('car', self.canvas, 1, 40, 2)
        car3 = vehicle('car', self.canvas, 1, 80, 3)
        car6 = vehicle('car', self.canvas, 2, -40, 7)
        car4 = vehicle('car', self.canvas, 2, 0, 4)
        car5 = vehicle('car', self.canvas, 2, 40, 5)
        bus = vehicle('bus', self.canvas, 2, 100, 6)

        v_list = [car1, car2, car3, car6, car4, car5, bus]
        g = GetNeighbour(v_list)
        self.vehicle_list = v_list

    def parallel_available_previous_missing(self):

        car2 = vehicle('car', self.canvas, 1, 40, 2)
        car3 = vehicle('car', self.canvas, 1, 80, 3)
        car4 = vehicle('car', self.canvas, 2, 0, 4)
        car5 = vehicle('car', self.canvas, 2, 40, 5)
        bus = vehicle('bus', self.canvas, 2, 100, 6)
        v_list = [car2, car3, car4, car5, bus]
        g = GetNeighbour(v_list)
        self.vehicle_list = v_list

    def parallel_and_previous_missing(self):

        car3 = vehicle('car', self.canvas, 1, 80, 3)
        car5 = vehicle('car', self.canvas, 2, 40, 5)
        bus = vehicle('bus', self.canvas, 2, 100, 6)
        v_list = [car3, car5, bus]
        g = GetNeighbour(v_list)
        self.vehicle_list = v_list

    def parallel_missing_previous_available(self):
        car1 = vehicle('car', self.canvas, 1, 0, 1)
        car3 = vehicle('car', self.canvas, 1, 80, 3)
        car5 = vehicle('car', self.canvas, 2, 40, 5)
        bus = vehicle('bus', self.canvas, 2, 100, 6)
        v_list = [car1, car3, car5, bus]
        g = GetNeighbour(v_list)
        self.vehicle_list = v_list














        # luck = ['car', 'bus']
        # for i in range(volume):
        #     v = random.randrange(0, 2)
        #     lane = random.randrange(1, 3)
        #     print(luck[v]+" in the ", lane)
        #     car = vehicle(luck[v], canvas, lane)
        #     if v == 0:
        #         self.car_list.append(car)
        #     else:
        #         self.bus_list.append(car)
        #
        # self.vehicle_list.extend(self.car_list)
        # self.vehicle_list.extend(self.bus_list)
        # shuffle(self.vehicle_list)






