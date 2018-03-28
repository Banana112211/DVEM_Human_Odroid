# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:42:34 2017

@author: root
"""

import find_gps
import time
def Find_Gyro_Input():
    i=0 #number to find_gps
    gps,state=find_gps.find_gps(i)
    while state!="success":
        time.sleep(1)
        i+=1
        gps,state=find_gps.find_gps(i)
        if i==10:
            print "Error Gyro"
    print i        
    return i
