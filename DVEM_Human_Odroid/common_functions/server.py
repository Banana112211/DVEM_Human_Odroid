#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import time
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind(('192.168.0.1', 55605))        # Bind to the port


while True:
   print("message1")
   s.listen(5)                 # Now wait for client connection.
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send(str(time.time()))
   print("message2")
c.close()                # Close the connection
