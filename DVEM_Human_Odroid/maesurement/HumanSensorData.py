# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 20:22:26 2017

@author: home
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 09:48:19 2017
@author: root
"""
# pip install hrv
import os
import time
import obd_recorder
import writecsv2
import datalogger
import client
import gyro
from multiprocessing import Process
import postprocessing
import pexpect
import getpass
import bluethooth_obd_connect

def log(name):
    
    try:
        '-------------------path anlegen-------------------------------------'   
        #Fahrer
        probantenname=name 
        data=dict()
        start=time.time()
        
        username ='odroid'# getpass.getuser()
        path='/media/'+username+'/DVEM_DATA'
        time_srt=str.replace(str(time.ctime(start)),':','_')
        if os.path.exists(path):
            path=path+'/logs/'+time_srt+'/'
        else:
            path='/home/'+username+'/Desktop/logs/'+time_srt+'/'
            
        os.makedirs(path)
        
        name=path+probantenname+"_"+time_srt
        '--------------------  ' 
        process_obd = Process(target=obd_recorder.startOBD, args=(name,))
        process_gyr=Process(target=gyro.gyro_sensor, args=(name,))
        process_sync=Process(target=client.client_receive, args=(55606,'192.168.0.1',name))
        
        gt=datalogger.inithializegt()  
        process_gyr.start()
        process_sync.start()
        time.sleep(3)
        process_obd.start()
        print(name)
        data["action"]=[]
        data["start"]=[]
        data["start"].append(start)
        
        
        writecsv2.writedatacsv(name,data,1)
        
        datalogger.readdata(1,gt,data)
        writecsv2.writedatacsv(name,data,0)
        output=str(data)+" \n"
        print(output)   
        
        while True:
            
            try:
                time.sleep(0.2)
                datalogger.readdata(1,gt,data)
                writecsv2.writedatacsv(name,data,1)
                output=str(data)+" \n"
                #print(output)
            
            except KeyboardInterrupt:
                gt.sendline("quit")
                
                print("Fahrversuch Beendet")
                data["end"]=[]
                data["end"].append(time.time())
                writecsv2.writedatacsv(name,data,0)
                process_gyr.terminate()
                process_obd.terminate()
                OBD.close()
                process_sync.terminate()
                postprocessing.main((name))
                 #pexpect.spawn("sudo rfcomm release all")
                break
    except:
        print('fehler end all')
        gt.sendline("quit")
                
        data["end"]=[]
        data["end"].append(time.time())
        writecsv2.writedatacsv(name,data,0)
        process_gyr.terminate()
        process_obd.terminate()
        process_sync.terminate()
        postprocessing.main((name))
        
       
    

    
if __name__ == "__main__":
    log("test")

 

