from enum import Enum, auto

CONNECTED_WAIT  = 0x01
CONNECTED_START = 0x02
PROMPT          = 0x03
ROCK            = 0x04
PAPER           = 0x05
SCISSORS        = 0x06
WIN             = 0x07
LOSE            = 0x08
TIE             = 0x09            
QUIT            = 0x0A
CONT            = 0x0B

inp_opc_map = {
    "R":ROCK,
    "P":PAPER,
    "S":SCISSORS,
    "Q":QUIT,
    "C":CONT
}
opc_inp_map = {v: k for k, v in inp_opc_map.items()}

class State(Enum):
    INPUT_GAME = auto()
    INPUT_CONT = auto()

def byte(i):
    return i.to_bytes(1,'little')
    
def str_to_bytes(string):
    return b''.join([ord(c).to_bytes(1,'little') for c in string])

def bytes_to_str(raw):
    return "".join([chr(x) for x in raw])