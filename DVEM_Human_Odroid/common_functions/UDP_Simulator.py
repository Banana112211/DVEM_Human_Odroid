# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 11:01:13 2017

@author: Gustav Willig
"""
import socket
import Write_Logfile

#==============
#todo: the received data need to be written to a log.txts
#todo: received time stampe give to Video_Frame_recored

def udp_simulator(queue):
    UDP_IP = "192.168.0.104"
    UDP_PORT = 3333       
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    Write_Logfile.logfile_schreiben("Current_time,WheelAngle,Accelrator,Brakepetal,SpeedInKilometers,PositionX,PositionY","Simulator")
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        #print ("received message:", data)
        Write_Logfile.logfile_schreiben(str(data),"Simulator")
        value=str(data).split(";")
        print value[0]
        while
        queue.put(value[0])
    #Step: Schliest das Quere-Objekt
    queue.close() #Schliest das Quere-Objekt
    queue.join_thread()#Gibt an  das alle in der Pipe befindlichen Element der Quere noch abgearbeitet werden sollen
    

