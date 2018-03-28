# -*- coding: utf-8 -*-
""" 
Created on Tue Sep  5 11:10:05 2017

@author: ubuntu
""" 
#HRM datalogger

import pexpect
import writecsv2
import time
import usb.core
import usb.util
VID = 0x16D0
PID = 0x06F9    

def inithializegt():
    """Funktion zum ini. des Bluethooth Dongle"""     
    gt = pexpect.spawn("sudo gatttool -i hci0 -b A0:9E:1A:1A:D4:3F  -I")

    gt.expect(r"\[LE\]>")

    gt.sendline("connect")
    gt.expect(["Connection successful.", r"\[CON\]"], timeout=30)
    gt.sendline("char-write-req 0x0013 0100")
    
    return gt
        
def oszi(gsr,protolab,count):
    gsr.append(0)
    x=[]
    x = protolab.read(0x81,770,1000)
        # Analog 1
    i=0
    for i in range(255):
        gsr[count]+=x[i] 
    gsr[count]=gsr[count]/256
    #print("messung:",count,"| ",gsr[count])
    return gsr

def readdata(t,gt,data):
         data.clear()
         hr=[]
         rr=[]
         gsr=[]
         hr_expect = "Notification handle = 0x0012" + " value: ([0-9a-f ]+)" 
         count=0
         protolab = usb.core.find(idVendor=VID, idProduct=PID) 
         #print("gattool")
         while count<t:
             try:
                 start=time.time()
                 #oszi(gsr,protolab,count)
                 #middle=time.time()
                 #time.sleep(0.5-(start-middle))
                 gt.expect(hr_expect)
              
                 datahex = gt.match.group(1).strip()
                 #print(datahex,count)
                 
                 #print(start-middle)
                 oszi(gsr,protolab,count)
                 data_hr = map(lambda x: int(x, 16), datahex.split(' '))
                 res = interpret(data_hr)
                 #print res
                 if res.has_key("rr"):
                     for i_rr in res["rr"]:

                         #print i_rr                                                  
                         rr.append(i_rr*1000/1024)
                 print res["hr"]
                 hr.append(res["hr"])
                 end=time.time()
                 
                 count+=1
                 #print(time.time()-start)
                 
             except KeyboardInterrupt:
                print("Received keyboard interrupt. Quitting cleanly.")
                usb.util.dispose_resources(protolab)
                data["hr"]=hr
                data["rr"]=rr
                data["gsr"]=gsr
                return data
                break   
        
         usb.util.dispose_resources(protolab) 
         data["hr"]=hr
         data["rr"]=rr
         data["gsr"]=gsr
         return data              

def log(t,name):

    maxtime=20  #alle 5s abspeichern 8h-> ~50 kb pro list

    data={}
    #name="test" #time.ctime()
    #writedata(hr,rr,name)
    try:
        gt=inithializegt()
        #--------festlegen wie lange augezeichnet wird: alle 5s abspeichern in csv
        if t<maxtime:
             
            readdata(t,gt,data)

            writecsv2.writedatacsv(name,data,1)
            
        if t>maxtime:
            runs=t/maxtime
            rest=t%maxtime
            i=0
            while i<runs :
               
                readdata(maxtime,gt,data)
                
                writecsv2.writedatacsv(data,name,1)
                i+=1
                
            readdata(t,gt,data)
            
            writecsv2.writedatacsv(data,name,1)
            
#           

    finally:
        gt.sendline("quit")
        

def interpret(data):
    """ 
    data is a list of integers corresponding to readings from the BLE HR monitor
    """ 

    byte0 = data[0]
    res = {}
    res["hrv_uint8"] = (byte0 & 1) == 0
    sensor_contact = (byte0 >> 1) & 3
    if sensor_contact == 2:
        res["sensor_contact"] = "No contact detected" 
    elif sensor_contact == 3:
        res["sensor_contact"] = "Contact detected" 
    else:
        res["sensor_contact"] = "Sensor contact not supported" 
    res["ee_status"] = ((byte0 >> 3) & 1) == 1
    res["rr_interval"] = ((byte0 >> 4) & 1) == 1

    if res["hrv_uint8"]:
        res["hr"] = data[1]
        i = 2
    else:
        res["hr"] = (data[2] << 8) | data[1]
        i = 3

    if res["ee_status"]:
        res["ee"] = (data[i + 1] << 8) | data[i]
        i += 2

    if res["rr_interval"]:
        res["rr"] = []
        while i < len(data):
            # Note: Need to divide the value by 1024 to get in seconds
            res["rr"].append((data[i + 1] << 8) | data[i])
            i += 2

    return res

def main():
    name="test" #time.ctime()
    t=10
    log(t,name)

if __name__ == '__main__':
    main()                
