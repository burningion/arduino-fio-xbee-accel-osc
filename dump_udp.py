from pythonosc import osc_message_builder
from pythonosc import udp_client 
import sys

# Create the socket, datagram mode, proprietary transport:
client = udp_client.UDPClient("192.168.1.148", 9000) 

while (1):
   try:
        line = sys.stdin.readline()
        msg = osc_message_builder.OscMessageBuilder(address = "/filter")
        msg.add_arg(line)
        msg = msg.build()
        client.send(msg)
        print(line)
   except:
       continue
