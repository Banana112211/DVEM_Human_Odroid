# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 17:17:47 2018

@author: root
"""
import pexpect

def connect_bluetooth_obd(): 
#    try:
        OBD=None
        pexpect.spawn("sudo rfcomm release all")# Sorgt dafuer das alle bestehenden Verbindungen geloest werden
        '----------------verbindung obd to serial-------------'
        i=0        
        while i<10:  
            sendstring="sudo rfcomm show "+ str(i)
    
            OBD=pexpect.spawn(sendstring)
            
            ret=OBD.readline()
            
            if "closed" in ret:
                i+=1
            if "rfcomm0: 00:0A:CD:30:8C:C7 -> 00:1D:A5:00:17:09 channel 1 connected" in ret:
                break
            if "No such device"  in ret:
                OBD= pexpect.spawn("sudo rfcomm connect "+str(i)+" 00:1D:A5:00:17:09 1")
                #OBD= pexpect.spawn("sudo rfcomm bind rfcomm"+str(i)+" 00:1D:A5:00:17:09 1")
                # sudo rfcomm bind rfcomm1 00:1D:A5:00:17:09 1
                # sudo sudo rfcomm connect 1 00:1D:A5:00:17:09 1
                # sudo rfcomm release all               
                OBD.expect("Connected")
                
                print OBD.readline()
                
                break
        return str(i),OBD
#    except:  
#            print "--------help----------------"
#            return "error_bluethooth_obd"