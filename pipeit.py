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

msg = OSC.OSCMessage("/hey")
msg.append('hello')
b = OSC.OSCClient()
b.connect(('192.168.1.148', 9000))
b.send(msg)
 
def int32(x):
  if x>0xFFFFFFFF:
    raise OverflowError
  if x>0x7FFFFFFF:
    x=int(0x100000000-x)
    if x<2147483648:
      return -x
    else:
      return -2147483648
  return x

try:
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
            if payload == "quit": 
                raise Exception, "quit received"
        msg = OSC.OSCMessage("/hey")
        list = payload.split(':')
        for reading in list:
            msg.append(int32(int(reading)), typehint='t')
        b = OSC.OSCClient()
        b.connect(('192.168.1.148', 9000))
        b.send(msg)

        print payload

except Exception, e:
    # upon an exception, close the socket:
    sd.close()
