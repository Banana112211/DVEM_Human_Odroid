# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 13:45:46 2017

@author: home
"""
# oszi(hautleitf)logger
 
import time
import usb.core
import usb.util
import writecsv

#import matplotlib.pyplot as plt

VID = 0x16D0
PID = 0x06F9

def messung(t):
    try:
        protolab = usb.core.find(idVendor=VID, idProduct=PID)    
#        if not protolab:
#            print("Could not find Protolab")
#            exit(1)
#        print("###################")
#        print("Found Protolab")
#        print("####################")
        count=0
        value=[]
        while (count < t):
            try:
                start=time.time()
                value.append(0)
                x=[]
                x = protolab.read(0x81,770,1000)
                    # Analog 1
                i=0
                for i in range(255):
                    value[count]+=x[i] 
                value[count]=value[count]/256
                print("messung:",count,"| ",value[count])
               # time.sleep(1)
                del x[:]
                dt=time.time()-start
                time.sleep(1-dt)
                count += 1
            except KeyboardInterrupt:
                break
        
    finally:usb.util.dispose_resources(protolab)        
    return value 

def gsr(t,name):
    try: 
        data={}
        value=messung(t)
    finally:    
        data["gsr"]=value
        time.sleep(1)
        writecsv.writedatacsv(data,name)
        
        
           
#        for i in range(len(value)):
#            plt.subplot(2, 1, 1)
#            plt.scatter(i, value[i]) 
        
def main():
    t=5
    name="test"
    gsr(t,name)
    

if __name__ == '__main__':
    main()

#while (count < 5):    
#    x = protolab.read(0x81,770,1000)
#    # Analog 1
#    for i in range(255):
#        plt.subplot(2, 1, 1)
#        plt.scatter(i, x[i]) 
#    # Analog 2
#    for i in range(255,511):        
#        plt.subplot(2, 1, 2)
#        plt.scatter(i, x[i])    
#    plt.show()
#    time.sleep(1)
#    count += 1
#usb.util.dispose_resources(protolab)
