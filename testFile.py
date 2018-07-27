from vehicle import vehicle
import time
from tkinter import *


tk = Tk()
canvas = Canvas(tk, width=600, height=400)
tk.title("testing")
canvas.pack()
ball = vehicle("bus", canvas)
print(type(ball))
ball2=vehicle("car", canvas)
for i in range(500):
    ball.move(1, 0)
    if i%10==0:
        k=2
    else:
        k=0
    ball2.move(2, k)
    tk.update()
    time.sleep(0.008)



tk.mainloop()