from mis_util import *
import socket
from mis_game import MIS_GAME
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from socket import error as GENERIC_SOCKET_ERROR
from threading import Thread, Semaphore
import time
import signal
import copy

serverPort = 9979
#attempt to create the socket
try:
    serverSocket = socket.socket(AF_INET,SOCK_STREAM)
    serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    serverSocket.settimeout(0.5)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
except GENERIC_SOCKET_ERROR as e:
    print("Could not create socket:",e)
    quit(1)

print('The server is ready to receive - Port ' + str(serverPort))

def on_exit(*args):
    print("\nExiting...")
    quit(0)
    
signal.signal(signal.SIGINT, on_exit)

cur_anim = 0 #for a pretty animation. Doubles as a polling timer
anims = ('|','/','—','\\')
matcher = []

while True:

    try:
        connectionSocket, addr = serverSocket.accept()
        connectionSocket.settimeout(0.5)
        matcher.append(connectionSocket)
        print("Connection on: {}: ({}/2)".format(addr, len(matcher)))
        
        time.sleep(0.5)
        
        if len(matcher) == 2: #refactor to allow 'n' connections (later)
                              #OK to strike every inactive only on attempt fill
            #make sure the first socket is alive
            try:
                r = matcher[0].recv(32)
                
                if not r: #closed!
                    matcher = [matcher[1]]
                    print("First player disconnected while waiting - reordering set...")
                    print("Players (1/2)")
                    continue 
            except socket.timeout:
                pass
            except ConnectionResetError:
                matcher = [matcher[1]]
                print("First player disconnected while waiting - reordering set...")
                print("Players (1/2)")
                continue

            MIS_GAME(list(matcher))
            matcher = []

    except socket.timeout:
        cur_anim = (cur_anim + 1) % len(anims)
        print("\rWaiting for connection... " + anims[cur_anim], end='')   