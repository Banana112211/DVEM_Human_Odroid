#!/usr/bin/env python
import os

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import getpass
import bluethooth_obd_connect
import pexpect


from obd_utils import scanSerial

class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []
        localtime = time.localtime(time.time())
        filename = path+"_car.csv"

        self.log_file = open(filename, "w", 128)
        self.log_file.write("Time,RPM,KMH,Throttle,Load,Fuel Status\n");

        for item in log_items:
            self.add_log_item(item)

        self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
        #log_formatter = logging.Formatter('%(asctime)s.%(msecs).03d,%(message)s', "%H:%M:%S")

    def connect(self):
        try:
            '----------------verbindung obd to serial-------------'
            port_status="OBD_not"
            value_obd=bluethooth_obd_connect.connect_bluetooth_obd()
            port_status="OBD_open"            
            print value_obd
            port_no=value_obd[0]
            """while port_no=="error_bluethooth_obd":
                port_no=bluethooth_obd_connect.connect_bluetooth_obd()  
            """'-------------------------------------------------------'   
            
            port="/dev/rfcomm"+str(port_no)
    
            self.port = obd_io.OBDPort(port, None, 2, 2)
            port_status="port_open"
            if(self.port):
                print "Connected to "+self.port.port.name
        except:
            if port_status=="port_open":
                print "error bluetooth connection_1"
                self.port.close()
                self.port = None
            
            elif  port_status=="OBD_open": 
                
                print "error bluetooth connection_2"
            elif port_status=="OBD_not":
                print "error bluetooth connection_3"
            
    def is_connected(self):
        return self.port
        
    def close(self):
        self.port.close()
        self.port = None
        return self.port
    
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
            
            
    def record_data(self):
        try:
            if(self.port is None):
                return None
            
            print "Logging started"
            
            while 1:
                localtime = datetime.now()
                current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
                log_string = current_time
                
                results = {}
                for index in self.sensorlist:
                    (name, value, unit) = self.port.sensor(index)
                    log_string = log_string + ","+str(value)
                    results[obd_sensors.SENSORS[index].shortname] = value;
                print log_string
                #gear = self.calculate_gear(results["rpm"], results["speed"])
                #log_string = log_string #+ "," + str(gear)
                self.log_file.write(log_string+"\n")
                
        except:
            self.port.close()
            self.port = None
            return "error"
    def calculate_gear(self, rpm, speed):
        if speed == "" or speed == 0:
            return 0
        if rpm == "" or rpm == 0:
            return 0

        rps = rpm/60
        mps = (speed*1.609*1000)/3600
        
        primary_gear = 85/46 #street triple
        final_drive  = 47/16
        
        tyre_circumference = 1.978 #meters

        current_gear_ratio = (rps*tyre_circumference)/(mps*primary_gear*final_drive)
        
        #print current_gear_ratio
        gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1] 
        return gear
    
def startOBD(name="test"):
    try:      
        #username = getpass.getuser()
        #== Aenderung: da Programm als username root bekommt wir jedoch odroid sind 
        username="odroid"
        logitems = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]
        o = OBD_Recorder(name, logitems)
        o.connect()
        print "connected"
    
        if not o.is_connected():
            print "Not connected"
        status_status=o.record_data()
        while status_status=="error":
            print"problem"
            o.connect()
            status_status=o.record_data()
            #time.sleep(1)
    except KeyboardInterrupt:
            o.close()

    #except:
    #    print SystemError

if __name__ == "__main__":
    startOBD("test")
