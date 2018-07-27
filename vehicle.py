"""
Created on Tue Jul 24 09:05:15 2018

@author: agrah
"""
import sys
import constant
import json


class vehicle:

    def __init__(self, type, canvas):

        self.type = type
        self.color = None
        self.dimension = None
        self.new_vehicel = None
        self.canvas = canvas

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
            self.new_vehicle = self.canvas.create_rectangle(0, 0, self.dimension[0], self.dimension[1], fill = self.color)

    def move(self, xspeed, yspeed):

        self.canvas.move(self.new_vehicle, xspeed, yspeed)




