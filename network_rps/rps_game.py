from rps_util import *
from threading import Thread
import socket

def mloop(ref):

    state = State.INPUT_GAME

    while True:
        #get input from other players
        inps = [None,None]
        ref.sock1.sendall(byte(PROMPT))
        ref.sock2.sendall(byte(PROMPT))
        while not inps[0] or not inps[1]:
            if not inps[0]:
                try:
                    raw = ref.sock1.recv(32)
                    if not raw: #socket *closed* unexpectedly
                        ref.sock2.sendall(byte(QUIT))
                        return
                    inps[0] = ord(raw)
                except socket.timeout:
                    pass
                except ConnectionResetError:
                    ref.sock2.sendall(byte(QUIT))
                    return
            
            if not inps[1]:
                try:
                    raw = ref.sock2.recv(32)
                    if not raw: #socket *closed* unexpectedly
                        ref.sock1.sendall(byte(QUIT))
                        return
                    inps[1] = ord(raw)
                except socket.timeout:
                    pass
                except ConnectionResetError:
                    ref.sock1.sendall(byte(QUIT))
                    return
    
        #handle quitters
        if inps[0] == QUIT or inps[1] == QUIT:
            ref.sock1.sendall(byte(QUIT))
            ref.sock2.sendall(byte(QUIT))
            break
        
        if state == State.INPUT_GAME: #playing
            #send opposing move back
            ref.sock1.sendall(byte(inps[1]))
            ref.sock2.sendall(byte(inps[0]))
            
            #calculate winner
            p1 = inps[0] - ROCK
            p2 = inps[1] - ROCK
            
            #lookup p1 and p2 in matrix
            p1_wmat = [
                [TIE,LOSE,WIN],   
                [WIN,TIE,LOSE],
                [LOSE,WIN,TIE]
            ]
            p1 = p1_wmat[p1][p2]
            
            #easy to find out p2's fate off of p1's
            p2_wmat = {
                WIN:LOSE,LOSE:WIN,TIE:TIE
            }
            p2 = p2_wmat[p1]
            
            #send winner back
            ref.sock1.sendall(byte(p1))
            ref.sock2.sendall(byte(p2))
            
            state = State.INPUT_CONT
            
        elif state == State.INPUT_CONT: #deciding to move on
            state = State.INPUT_GAME    #nothing to do here...
       

class RPS_GAME:
    def __init__(self, sock1, sock2):
        self.sock1 = sock1
        self.sock2 = sock2
        self.t = Thread(target=mloop,args=(self,))
        self.t.daemon = True
        self.t.start()