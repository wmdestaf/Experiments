import tkinter as tk
from tkinter import ttk
from math import floor, sqrt, sin, cos, radians
from mis_util import *
import socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from socket import error as GENERIC_SOCKET_ERROR
from threading import Thread, Semaphore
import re
import time
import signal

FLOCAL = True

cur_anim = 0 #for a pretty animation. Doubles as a polling timer
anims = ('|','/','—','\\')

def acquire_connection(): 
    global cur_anim, anims, myID
  
    #Request useer for server IP
    if not FLOCAL:
        while True:
            serverName = input('Connect where? ')
            if not serverName:
                continue
            break
    else:
        serverName = 'localhost'

    serverPort = 9979

    #Establish a socket
    try:
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)
        clientSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        clientSocket.settimeout(0.5)
    except GENERIC_SOCKET_ERROR as e:
        print("Could not establish socket -",e)
        quit(1)
        
    #Connect the socket to the server
    try:
        clientSocket.connect((serverName,serverPort))
    except GENERIC_SOCKET_ERROR as e:
        print("Could not connect to server -",e)
        quit(1)
        
    while True: #wait for our 'all-clear'
        try:
            myID = int.from_bytes(clientSocket.recv(32),'little',signed=True)
            break
        except socket.timeout:
            cur_anim = (cur_anim + 1) % len(anims)
            print("\rWaiting for other player...", anims[cur_anim], end='')
            pass
        
    print("\r" + (" ") * 80)
    return clientSocket
    
def synchronize_in():
    global clientSocket, haveLatestPos, latest_pos, latest_dydx
    
    while True:
        try:
            frame = clientSocket.recv(64)
        except socket.timeout:
            continue
           
        opcode = int.from_bytes(frame[  : 4],'little',signed=True)
        if opcode == MOVEMENT:
            x  = int.from_bytes(frame[4 : 8],'little',signed=True)
            y  = int.from_bytes(frame[8 :12],'little',signed=True)
            dx = int.from_bytes(frame[12:16],'little',signed=True)
            dy = int.from_bytes(frame[16:20],'little',signed=True)
            iD = int.from_bytes(frame[20:24],'little',signed=True)
            latest_pos[iD]  = [x,y]
            latest_dydx[iD] = [dx,dy]
    
#send our position and dy/dx to the server
def synchronize_out(dx,dy):
    global clientSocket
    clientSocket.sendall( MOVEMENT.to_bytes(4,'little',signed=True) + 
                          dx.to_bytes(4,'little',signed=True) + dy.to_bytes(4,'little',signed=True) )

def game_loop():
    global canv, keydowns, player_img
    global latest_pos, latest_dydx, haveLatestPos, myID
    global r
    global theta
   
    #send current movement inputs
    dx = keydowns[2] - keydowns[0]
    dy = keydowns[3] - keydowns[1]
    synchronize_out(dx,dy)
    
    #calculate movement based off what the server gave us

    for iD, pos in latest_pos.items():
        canv.coords(imgs[iD], pos[0] - floor(r/2), pos[1]  - floor(r/2), 
                              pos[0] + floor(r/2), pos[1]  + floor(r/2))
        
        if iD == myID:
            canv.xview_moveto(0)
            canv.yview_moveto(0)
            canv.xview_scroll((300-250) + pos[0],tk.UNITS)
            canv.yview_scroll((300-250) + pos[1],tk.UNITS)
            
            head_x = floor(pos[0] + r/3 * cos(radians(theta)))
            head_y = floor(pos[1] + r/3 * sin(radians(theta)))
            
            canv.coords(myView, head_x - floor(r/8), head_y - floor(r/8), 
                                head_x + floor(r/8), head_y + floor(r/8))

    canv.update()
    canv.after(25, game_loop)

def keyup(e):
    #print('up', e.keysym_num)
    k = e.keysym_num
    if k >= 65361 and k <= 65364: #arrow keys
        keydowns[k-65361] = 0
    
    
def keydown(e):
    #print('down', e.keysym_num)
    k = e.keysym_num
    if k >= 65361 and k <= 65364: #arrow keys
        keydowns[k-65361] = 1

def motion(event):
    global old, sensitivity, theta
    
    x, y = event.x, event.y
    if not old:
        old = [x, y]
        
    delta_x = x - old[0]
    delta_y = y - old[1]
    old = [x, y]
    
    theta += delta_x * sensitivity
    
    #print('{}, {}'.format(delta_x, delta_y))

def click_fire(*args):
    global theta, clientSocket, last_fire_time #hitscan
    print(time.time(), last_fire_time, time.time() - last_fire_time)
    if time.time() - last_fire_time < 2.5:
        print("Can't fire yet!")
        return
    last_fire_time = time.time()
    clientSocket.sendall( MISSILE.to_bytes(4,'little',signed=True) + theta.to_bytes(4,'little',signed=True) )

def set_sensitivity_(s):
    global sensitivity
    sensitivity = s

def set_sensitivity(*args):
    global root, sensitivity
    
    dialog = tk.Toplevel(root)
    dialog.title("Sensitivity")
    dialog.geometry("300x150")
    
    slider = tk.Scale(dialog, from_=0.5, to_=10, orient=tk.HORIZONTAL, 
                      tickinterval=0.5, length=250, command=lambda a: set_sensitivity_(a))
    slider.set(sensitivity)
    slider.pack()
    close  = ttk.Button(dialog, text="Close", command=lambda *a: dialog.destroy())
    close.pack()

if __name__ == "__main__":
    clientSocket = acquire_connection()

    #main window
    s_width,s_height = 500,500
    root = tk.Tk()
    ttk.Style(root).theme_use('alt')
    root.title("Shooter")
    root.resizable(False,False)
    root.geometry(str(s_width) + 'x' + str(s_height))
    
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)
    root.bind('<Motion>', motion)
    root.bind('<Button-1>', click_fire)
    
    #canvas
    canv = tk.Canvas(root, bg='green', height=500, width=500, scrollregion=(-300,-300,300,300))
    canv["xscrollincrement"] = 1
    canv["yscrollincrement"] = 1
    #scroll the canvas to fit around our position '0,0' as the center
    canv.xview_scroll(-250, tk.UNITS)
    canv.yview_scroll(-250, tk.UNITS)
    canv.grid()

    #MENU
    menubar = tk.Menu(root)
    configmenu = tk.Menu(menubar, tearoff=0)
    configmenu.add_command(label="Sensitivity", command=set_sensitivity, accelerator="S")
    menubar.add_cascade(label="Config", menu=configmenu)
    root.config(menu=menubar)

    #GAME VARIABLES
    
    #we'll just say 4 players for now. TODO: FIXME
    
    keydowns = [0]*4
    haveLatestPos = False
    latest_pos  = {n:[0, 0] for n in range(4)}
    latest_dydx = {n:[0, 0] for n in range(4)}
    old = None
    theta = 0
    sensitivity = 1
    last_fire_time = 0
    
    #existent images
    canv.create_rectangle(-100,-100,-90,-90)
    canv.create_rectangle(90,100,100,90)
    
    canv.create_polygon([-250,-250,-250,250,250,250,250,-250],fill='',outline='black')
    
    #player image
    r = 50
    colors = ['black','cyan','red','orange']
    imgs = {n: canv.create_oval(-floor(r/2) - 1000, - floor(r/2), +floor(r/2) - 1000, +floor(r/2), outline=colors[n]) for n in range(4)}
    myView = canv.create_oval(-floor(r/8), -floor(r/8), floor(r/8), floor(r/8));
    game_loop()
    
    
    in_recv = Thread(target=synchronize_in)
    in_recv.start()
    root.mainloop()