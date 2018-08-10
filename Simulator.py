from ThesisImplementation.vehicleGenerator import vehicleGenerator
from win32api import GetSystemMetrics
from tkinter import *
import time


crashed = False
tk = Tk()
canvas = Canvas(tk, width=GetSystemMetrics(0), height=GetSystemMetrics(1))
tk.title("Simulator")
canvas.pack()
vg = vehicleGenerator(canvas, 2)
v = vg.vehicle_list

while not crashed:
    for i in v:
        i.move()
    tk.update()
    time.sleep(.01)

tk.mainloop()


