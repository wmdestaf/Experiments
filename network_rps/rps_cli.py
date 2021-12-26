from rps_util import *
import socket
from socket import AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from socket import error as GENERIC_SOCKET_ERROR
from threading import Thread, Semaphore
from _thread import interrupt_main
import re
import time
import signal

#Request useer for server IP
while True:
    serverName = input('Connect where? ')
    if not serverName:
        continue
    break

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

def on_exit(*args):
    print("\nKilled.")
    clientSocket.shutdown(socket.SHUT_RDWR)
    clientSocket.close()
    quit(0)
    
signal.signal(signal.SIGINT, on_exit)

anims = ('|','/','—','\\')
cur_anim = 0

state = State.INPUT_GAME

def get_conf_lk(prompt, acceptable):
    while True:
        x = input(prompt + " [" + "|".join(acceptable.upper()) + "] ")
        if not x or x[0].lower() not in acceptable:
            continue
        return x[0].upper()

#client maintenence of game state
played = 0
won = 0
lost = 0
tied = 0

while True:
    try:
        res = clientSocket.recv(1)
    except socket.timeout:
        print("\rWaiting for other player... " + anims[cur_anim], end='')
        cur_anim = (cur_anim + 1) % len(anims)
        continue
    except ConnectionResetError:
        print("The server unexpectedly reset the connection.")
        break
        
    if not res:
        print("The server unexpectedly closed the connection.")
        break
        
    #handle response btye
    res = ord(res)
    if res == CONNECTED_WAIT:
        print("\rConnected." + (" " * 20))
    elif res == CONNECTED_START:
        print("\rStarting game..." + (" " * 20))
    elif res == PROMPT and state == State.INPUT_GAME:
        inp = get_conf_lk("\r(R)ock, (P)aper, (S)cissors, (Q)uit?", "rpsq")
        clientSocket.sendall(byte(inp_opc_map[inp]))
        state = State.INPUT_CONT
    elif res == PROMPT and state == State.INPUT_CONT:
        #an appropriate place to display player stats
        print("Played {} (Won {}, Lost {}, Tied {}) (Win Pct: {:3.3f}%)".format(played,won,lost,tied,(100 * (won/played))))
        
        inp = get_conf_lk("\r(C)ontinue, or (Q)uit?","cq")
        clientSocket.sendall(byte(inp_opc_map[inp]))
        state = State.INPUT_GAME
    elif res == ROCK:
        print("The opponent played: 'Rock'")
    elif res == PAPER:
        print("The opponent played: 'Paper'")
    elif res == SCISSORS:
        print("The opponent played: 'Scissors'")
    elif res == WIN:
        print("You've won!")
        won += 1
        played += 1
    elif res == LOSE:
        print("You've lost.")
        lost += 1
        played += 1
    elif res == TIE:
        print("Tie...")
        tied += 1
        played += 1
    elif res == QUIT:
        print("\rOne or more players have quit - The game has concluded.")
        clientSocket.shutdown(socket.SHUT_RDWR)
        clientSocket.close()
        break
    
    