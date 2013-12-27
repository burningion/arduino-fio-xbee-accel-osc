 # Include the socket and select modules: 
import xbee
import zigbee
import struct
from socket import *
from select import * 
import time
import OSC
import ctypes

# Create the socket, datagram mode, proprietary transport:
sd = socket(AF_XBEE, SOCK_DGRAM, XBS_PROT_TRANSPORT)
# Bind to endpoint 0xe8 (232) for ZB/DigiMesh, but 0x00 for 802.15.4
sd.bind(("", 0xe8, 0, 0))
# Configure the socket for non-blocking operation:
sd.setblocking(0) 

OSC_SERVER_IP = "192.168.1.148" # CHANGE TO YOUR OSC SERVER
OSC_SERVER_PORT = 9000 # CHANGE TO YOUR OSC SERVER PORT

b = OSC.OSCClient()
b.connect((OSC_SERVER_IP, OSC_SERVER_PORT))


''' Uncomment this below to diagnose your OSC connection first.

msg = OSC.OSCMessage("/hey")
msg.append('hello')
b.send(msg)
''' 

# Initialize state variables: 
payload = ""
src_addr = () 
 
    # Forever: 
 
while 1: 
    # Reset the ready lists:
    rlist, wlist = ([], [])
    if len(payload) == 0:
            # If the payload buffer is empty,
            # add socket to read list: 
        rlist = [sd]
 
    else: 
        # Otherwise, add the socket to the
        # write list: 
        wlist = [sd] 
 
 
    # Block on select: 
    rlist, wlist, xlist = select(rlist, wlist, []) 
 
 
    # Is the socket readable? 
    if sd in rlist: 
        # Receive from the socket: 
        payload, src_addr = sd.recvfrom(255)
        # If the packet was "quit", then quit:
        msg = OSC.OSCMessage("/hey")
        print str(payload)
        lister = payload.split(':')
        if len(lister) != 3:
            continue # bad data, man. don't try and save it, just move on
        for reading in lister:
            msg.append(int(reading), typehint='i')
        b.send(msg)
    payload = []

    time.sleep(.05)
