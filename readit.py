import xbee 
import zigbee
import struct 
import socket
import time

TESTADDR = '[00:13:a2:00:40:79:e6:d8]!'

def xbee_parse_inputs(data):
    if len(data) % 2 == 0:
        sets, datamask, analogmask = struct.unpack("!BHB", data[:4])
        data = data[4:]
 
    else:        
        sets, mask = struct.unpack("!BH", data[:3])
        data = data[3:]
        datamask = mask % 512 # Move the first 9 bits into a separate mask
        analogmask  = mask >> 9 #Move the last 7 bits into a separate mask
 
    retdir = {}
 
    if datamask:
        datavals = struct.unpack("!H", data[:2])[0]
        data = data[2:]
 
        currentDI = 0
        while datamask:
            if datamask & 1:
                retdir["DIO%d" % currentDI] = datavals & 1
            datamask >>= 1
            datavals >>= 1
            currentDI += 1
 
    currentAI = 0
    while analogmask:
        if analogmask & 1:
            aval = struct.unpack("!H", data[:2])[0]
            data = data[2:]
 
            retdir["AI%d" % currentAI] = aval
        analogmask >>= 1
        currentAI += 1
 
    return retdir


sd = socket.socket(socket.AF_XBEE, socket.SOCK_DGRAM, socket.XBS_PROT_TRANSPORT) 
sd.bind(("", 0xe8, 0, 0))   # Bind to endpoint 0xe8 (232):

rlist, wlist = ([], [])
    
    
while (1):
  print "Waiting for packet..."
  time.sleep(.3)
  payload, src_addr = sd.recvfrom(255) # This is blocking

  print payload
  clean_input = xbee_parse_inputs(payload)
#  print "Got packet: %s " % clean_input
