import requests as r
import time
import math
from graphics import *

base = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
key = "66a905986f69f47aa8a8f9eaee03aebb"
clock_sz = 100 #px

#force input
city = input("City: ")
while not city:
    city = input("City: ")
    
url = base.format(city,key)
res = r.get(url)
#match...case is very new, so consider older python 3.x
if res.status_code != 200:
    if res.status_code == 404:
        print("Unrecognized City:", city)
    else:
        print("Error: Server responded with status", status_code)
    quit(1)

json = res.json()

sun = time.localtime(json['sys']['sunrise'])
sst = time.localtime(json['sys']['sunset'])
win = GraphWin("Sunrise and Sunset", 2 * clock_sz, clock_sz * 1.5)

#clocks
for clk in ((sun,0),(sst,1)):
    height_center = clock_sz/2
    width_center = height_center + (clk[1] * clock_sz)
    hour_arm = height_center * 0.6
    min_arm  = height_center * 0.9
    
    Circle(Point(width_center,height_center), height_center).draw(win)
    ang = ((clk[0].tm_hour % 12) / 12) * math.tau - (math.pi/2)
    Line(Point(width_center,height_center),Point(width_center+(math.cos(ang)*hour_arm), height_center+(math.sin(ang)*hour_arm))).draw(win)
    ang = (clk[0].tm_min / 60) * math.tau - (math.pi/2)
    Line(Point(width_center,height_center),Point(width_center+(math.cos(ang)*min_arm), height_center+(math.sin(ang)*min_arm))).draw(win)

    txt = Text(Point(clock_sz,int(clock_sz*(23/20)) + (2*clock_sz*0.1*clk[1])),time.asctime(clk[0]) + " (EST)")
    txt.setSize(int(clock_sz*0.1))
    txt.draw(win)
    
try:
    win.getMouse()
except:
    pass