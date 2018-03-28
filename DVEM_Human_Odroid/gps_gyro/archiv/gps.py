#General informationen:
#If you enter the following  code line in the cmd, you will get the port information of the gps-device "python -m serial.tools.list_ports"

import serial
import os
#=======#Change the working direction to "common_functions" and back
dir_path = os.path.dirname(os.path.realpath(__file__)) #real current working direction
dir_path_seperated=str(dir_path).split("/")# divide the current working direction
common_functions=str(dir_path_seperated[0])+"/"+str(dir_path_seperated[1])+"/"+str(dir_path_seperated[2])+"/"+str(dir_path_seperated[3])+"/"+"common_functions"
os.chdir(common_functions)
#common load modul
import Write_Logfile
os.chdir(dir_path)
#==============

#1.Step:Ensure that the gps-device is succesfull conected to the odroid
gps=serial.Serial("/dev/ttyACM0",baudrate=9600) # Durch Erhoehung der Baudrate und der gleichzeitigen Erhoehung der Freqeunz im Sender koennen mehr Signale gesnedet werden

#=======================
#=======================
#print(gps) if you print the gps signal and not an error message occur 
Write_Logfile.logfile_schreiben("Current_Time,Latitude,Latitude_direction,Longitude,Longitude_direction,Number_of_satellites","gps")
while True:
    line=gps.readline()
    data=line.split(",")
    
    if data[0]=='$GPGGA':
        if data[6]!="":  #6 posion prvoides information about Fix quality of the signal
            current_time=str(int(data[1][:2])+2)+":"+data[1][2:4]+":"+data[1][4:6]
            latitude=str(int(data[2][:2])+float(data[2][2:])/60)+","+str(data[3])
            longitude=str(int(data[4][:3])+float(data[4][3:])/60)+","+str(data[5])
            Number_of_satellites=data[7]
            message=str(current_time+","+latitude+","+longitude+","+Number_of_satellites) #the whole contain must converted to a string!
            Write_Logfile.logfile_schreiben(message,"gps")
            
    
    
#    #===== The following lines help to test the programm
#    if data[0]=='$GPGGA':
#        if data[6]!="":  #6 posion prvoides information about Fix quality of the signal
#           print "Current Time:{}".format(str(int(data[1][:2])+2)+":"+data[1][2:4]+":"+data[1][4:6])
#           print "Latitude: {0},{1}".format(int(data[2][:2])+float(data[2][2:])/60,data[3]) 
#           # ddmm.mmmm format for latitude and in dddmm.mmmm for longitud
#           #Conver to number   https://www.experts-exchange.com/questions/22112629/Converting-NMEA-sentence-Latitude-and-Longitude-to-Decimal-Degrees.html
#           print "Longitude: {0},{1}".format(int(data[4][:3])+float(data[4][3:])/60,data[5])
#           #Number of satellites being tracked
#           print "Number of satellites: {}".format(data[7])
           
#Die Daten erden 
       