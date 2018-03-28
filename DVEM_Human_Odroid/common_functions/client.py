#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import Write_Logfile
import time

def client_receive(ip='192.168.0.1',port=55606):
    Write_Logfile.logfile_schreiben("Odroid2_time,Odorid_2_192.168.0.2_unixtime,Odorid_1_192.168.0.1_unixtime","Sycronisation")
    print "client is online"
    while True:
        s = socket.socket()   
        s.connect((ip, port))
        Write_Logfile.logfile_schreiben(str(time.asctime())+","+str(time.time())+","+str(s.recv(1024)),"Sycronisation")
        #print "finish"
        s.close()                    # Close the socket when done


if __name__=="__main__":
    client_receive()
