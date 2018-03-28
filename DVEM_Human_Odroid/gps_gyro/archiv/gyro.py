 # -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 18:51:52 2017

@author: home
"""

" The following code is based on https://github.com/withrobot/myAHRS_plus/tree/master/common_python/pygame/shooting/myahrs_plus.py"
"Author: Gustav"

import sys, time, thread, serial, traceback, os
import numpy as np
import writecsv2
import find_gyro
#=======#Change the working direction to "common_functions" and back
"""dir_path = os.path.dirname(os.path.realpath(__file__)) #real current working direction
dir_path_seperated=str(dir_path).split("/")# divide the current working direction
common_functions=str(dir_path_seperated[0])+"/"+str(dir_path_seperated[1])+"/"+str(dir_path_seperated[2])+"/"+str(dir_path_seperated[3])+"/"+"common_functions"
os.chdir(common_functions)
#common load modul
import Write_Logfile
os.chdir(dir_path)
#=============="""

class MyAhrsPlus(object):
    def __init__(self, serial_device="/dev/ttyACM0", baudrate=115200, *args, **kwargs):
        super(MyAhrsPlus, self).__init__(*args, **kwargs)
        
        try:
            serial_port = serial.Serial(serial_device, baudrate, timeout=0)
        except serial.serialutil.SerialException:
            print ('Can not open serial port(%s)'%(serial_device))
            serial_port = None 
            traceback.print_exc()
            return     
    
        self.serial_port = serial_port
       
        # Orientation 
        self.euler_angle_deg = (0, 0, 0)
        self.yaw_offset = 0
        
        # Imu 
        self.acceleration = (0, 0, 0)
        self.angular_rate = (0, 0, 0)
        
        # Receiver 
        self.rcv_count = 0
        self.response_message = None 
                   
        def _receiver():
            stream = ""
            while(True):
                data = self.serial_port.read(1024)
                if(len(data) == 0):
                    time.sleep(0.01)
                else:
                    stream += data
                                        
                    while(True):
                        segments = stream.split('\n', 1)      
                        if(len(segments) < 2):                            
                            break
                        else:
                            line = segments[0]
                            stream = segments[1]   
                                                        
                            if(len(line) == 0):
                                continue                
    
                            if(line[0] == '~'):
                                # response message
                                self.response_message = line                                 
                            else:
                                # data message
                                items = self._parse_data_message_rpyimu(line)                            
                                if(items):
                                    sequence_number, roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature = items
                                    #print '## roll %.2f, pitch %.2f, yaw %.2f, ax %.4f, ay %.4f, az %.4f, gx %.4f, gy %.4f, gz %.4f, mx %.4f, my %.4f, mz %.4f, temp %.1f'%(roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature)
                                    
                                    yaw = yaw - self.yaw_offset
                                    
                                    self.euler_angle_deg = (roll, pitch, yaw)
                                    self.acceleration = (accel_x, accel_y, accel_z)
                                    self.angular_rate = (gyro_x, gyro_y, gyro_z)
                                    
                                    self.rcv_count += 1
                    
        self.thread = thread.start_new_thread(_receiver, ()) 

        #
        # Get version 
        #
        rsp = self._send_command('version')
        print (rsp) 
        
        #
        # Data transfer mode : ASCII, TRIGGER 
        #
        rsp = self._send_command('mode,AC')
        print (rsp)  
        
        #
        # Select output message type 
        #
        rsp = self._send_command('asc_out,RPYIMU')
        print (rsp)    

        #
        # speed 
        #
        rsp = self._send_command('divider,2')
        print (rsp)   

        #
        # waiting for first data message 
        #        
        self.rcv_count = 0
        while(self.rcv_count == 0):
            time.sleep(0.1)
        
        
    def read_euler(self):
        return self.euler_angle_deg

    def read_acceleration(self):
        return self.acceleration
    
    
    def read_angular_rate(self):
        return self.angular_rate    
    
    
    def set_yaw_offset(self, yaw):
        self.yaw_offset = yaw 
    
    
    def _send_command(self, cmd_msg):
        cmd_msg = '@' + cmd_msg.strip()
        crc = 0
        for c in cmd_msg:
            crc = crc^ord(c)
            
        self.response_message = None 
        cmd_msg = cmd_msg + '*%02X'%crc + '\r\n'
        self.serial_port.write(cmd_msg)
        
        print( "%s"%(cmd_msg.strip()))
        
        #
        # wait for response 
        #    
        if(cmd_msg != '@trig'):
            while(self.response_message == None):
                time.sleep(0.1)
            return self.response_message.strip()
    
    
    def _parse_data_message_rpyimu(self, data_message):
        # $RPYIMU,39,0.42,-0.31,-26.51,-0.0049,-0.0038,-1.0103,-0.0101,0.0014,-0.4001,51.9000,26.7000,11.7000,41.5*1F
        
        data_message = (data_message.split('*')[0]).strip() # discard crc field  
        fields = [x.strip() for x in data_message.split(',')]
        
        if(fields[0] != '$RPYIMU'):
            return None
        
        sequence_number, roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature = (float(x) for x in fields[1:])
        return (int(sequence_number), roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature)



def gyro_sensor(name=str(),queue=None):
    name=name+"_gyr"
    i=find_gyro.Find_Gyro_Input()
    serial_device = '/dev/ttyACM'+str(i)
    ahrs = MyAhrsPlus(serial_device)
        
    yaw_list = []
    for i in range(10):
        e = ahrs.read_euler();
        yaw_list.append(e[2])
    
    yaw_offset = np.mean(yaw_list)
    
    print( "Yaw offset %.2f"%(yaw_offset))
    
    keys=['roll', 'pitch', 'yaw', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z','time','time_sim']
    
    g_data=dict([(key, []) for key in keys])
    writecsv2.writedatacsv(name,g_data,0)
    nr=0
    #Write_Logfile.logfile_schreiben("roll, pitch, yaw,nr,time","gyro")
    while(True):
        try:
            now=time.asctime()
            e = ahrs.read_euler();
            f=ahrs.read_acceleration()
            g=ahrs.read_angular_rate()
            for c in range(2):
                g_data[keys[c]].append(e[c])
                g_data[keys[c+3]].append(f[c])
                g_data[keys[c+6]].append(g[c])
            g_data[keys[9]].append(time.time())
            if queue:
                g_data[keys[10]].append(queue.get())
            writecsv2.writedatacsv(name,g_data,1)
                
            print( "EULER ANGLE (%.2f, %.2f, %.2f )"%e)
            message=str(str(e[0])+","+str(e[1])+","+str(e[2])+","+str(nr)+","+str(now)) #the whole contain must converted to a string!
            #Write_Logfile.logfile_schreiben(message,"gyro")
            
            print(message)
            nr+=1
            time.sleep(0.05)
        except KeyboardInterrupt:
            break
    
    ahrs.serial_port.close()


#=======Delete after successfull testing!
if __name__ == '__main__':
    gyro_sensor("test")
