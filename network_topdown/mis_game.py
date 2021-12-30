from mis_util import *
from threading import Thread
import socket
from math import floor, sqrt

def clamp_and_bound(pos, dx, dy, bounds):
    if len(bounds) != 4:
        raise ValueError
        
    min_x = bounds[0]
    max_x = bounds[1]
    min_y = bounds[2]
    max_y = bounds[3]
    
    #should dx push the position out of bounds, reduce dx to push to *exactly* the bound
    if pos[0] + dx < min_x:
        dx = min(0,min_x - pos[0])
    elif pos[0] + dx > max_x:
        dx = min(0,max_x - pos[0])
        
    #should dy '         '
    if pos[1] + dy < min_y:
        dy = min(0,min_y - pos[1])
    elif pos[1] + dy > max_y:
        dy = min(0,max_y - pos[0])
        
    return (dx, dy)

def detect_and_avoid_collisions(pos, dx, dy, boxes):
    for box in boxes:
        #if moving in the x direction causes a collision on the left and right...
        tent_x = pos[0] + dx
        tent_y = pos[1]
        if collide := box.halo_collide(tent_x,tent_y):
            if collide[0] or collide[2]:
                dx = 0

        #if moving in the y direction causes a collision on the top or bottom...
        tent_x = pos[0]
        tent_y = pos[1] + dy
        if collide := box.halo_collide(tent_x,tent_y):
            if collide[1] or collide[3]:
                dy = 0
                
        #if moving diagonally causes a collision on the corner...
        tent_x = pos[0] + dx
        tent_y = pos[1] + dy
        if collide := box.halo_collide(tent_x,tent_y):
            if any(collide[i] and collide[(i+1)%4] for i in range(4)):
                dx = 0
                dy = 0
            
    return dx, dy
 
def mloop(ref, me, others, mypos, myID):

    me.send(myID.to_bytes(4,'little',signed=True))
    #TODO: RATELIMIT SPEED OF LOOP TO 1/4 SECOND

    xspeed = 5
    yspeed = 5
    INV2 = 1 / sqrt(2) 

    while True:
        try:
            frame = me.recv(64)
        except socket.timeout:
            continue
         
        opcode = int.from_bytes(frame[:4],'little',signed=True)
        if opcode == MOVEMENT:
            #extract
            dx = int.from_bytes(frame[4:8] ,'little',signed=True)
            dy = int.from_bytes(frame[8:12],'little',signed=True)

            #calculate
            diag = 1 if not (dx and dy) else INV2
            dx_p = floor(xspeed * dx * diag)
            dy_p = floor(yspeed * dy * diag)
            dx_p, dy_p = detect_and_avoid_collisions(mypos,dx_p,dy_p,ref.obj_map)
            #dx_p, dy_p = clamp_and_bound(mypos,dx_p,dy_p,[-250,250,-250,250])
             
            #move
            mypos[0] += dx_p
            mypos[1] += dy_p
            
            #send back
            me.sendall( MOVEMENT.to_bytes(4,'little',signed=True) +
                        mypos[0].to_bytes(4,'little',signed=True) + mypos[1].to_bytes(4,'little',signed=True) +
                            dx_p.to_bytes(4,'little',signed=True) +     dy_p.to_bytes(4,'little',signed=True) +
                            myID.to_bytes(4,'little',signed=True)      
                      )
             
            for other in others:
                other.sendall( MOVEMENT.to_bytes(4,'little',signed=True) +
                               mypos[0].to_bytes(4,'little',signed=True) + mypos[1].to_bytes(4,'little',signed=True) +
                                   dx_p.to_bytes(4,'little',signed=True) +     dy_p.to_bytes(4,'little',signed=True) +
                                   myID.to_bytes(4,'little',signed=True)      
            )
        elif opcode == MISSILE:
            pass

class MIS_GAME:
    def __init__(self, socks):
        self.obj_map = obj_map1
        self.socks = socks
        self.poss = [[0,0] for sock in socks]
        self.threads = [Thread(target=mloop,args=(self, sock, list(filter(lambda x: x != sock, socks)),self.poss[idx],idx)) 
                        for idx, sock in enumerate(socks)]
        for t in self.threads:
            t.daemon = True
            t.start()