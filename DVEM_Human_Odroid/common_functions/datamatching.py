# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:17:58 2017

@author: home
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 17:39:42 2017

@author: home
"""

import writecsv2

#==============================================================================
import tkinter as tk#Tkinter in 2.7
from tkinter import filedialog #tkFileDialog

def main(filename="13_11/jago_Simu Mon Nov 13 13_43_38 2017.csv"):
    
    timepoint_sec=25.5
    
    delta_gyr=0.05
    dataset_gyr=int(timepoint_sec/delta_gyr)
    dataout=dict()
    #-----------------------------------read data as dict--------------------
    filename=filename.split(".")[0]
    filename_gyr=filename+"_gyro.csv"
    filename_sync=filename+"_sync.txt"
    filename=filename+".csv"
    
    data=writecsv2.csvreader(filename,0)
    data_gyr=writecsv2.csvreader(filename_gyr,0)
    data_sync=writecsv2.csvreader(filename_sync,0)
    #-----------------------------------Daten splitten in hr,gsr und rr-----------
    split_idx = 7
    data_hr = dict(list(data.items())[:split_idx])
    data_rr = dict(list(data.items())[split_idx:])
    data_rr["rr"]=(data_hr.pop("rr"))
    #----------------------------------time keys&indices festlegen---------------------------
    start=float(data_gyr["time"][0])
    datasets=len(data_gyr["time"])
    TimeKey_sync="Odroid_time"
    TimeKey_hr="01_time (s)"
    TimeKey_rr="time_rr"
    end=start+datasets*delta_gyr
    
    index_sync=int()
    index_hr=int()
    index_rr=int()
    #---------------------------------times vergleichen-----------------------------------
    while abs(float(data_gyr["time"][dataset_gyr]) -float( data_sync[TimeKey_sync][index_sync]))>delta_gyr:
        index_sync+=1
    while abs(float(data_gyr["time"][dataset_gyr]) -(start+float( data_hr[TimeKey_hr][index_hr])))>0.5:
        index_hr+=1
    while abs(float(data_gyr["time"][dataset_gyr]) -(start+float( data_rr[TimeKey_rr][index_rr])))>0.5:
        index_rr+=1
    #--------------------------------daten zu Zeitpunkt timepoint_sec in ausgabe dict schieben-------------
    for key in data_hr:
       try:dataout[key]=data_hr[key][index_hr]
       except:next
    for key in data_rr:
        try:dataout[key]=data_rr[key][index_rr]
        except: next
    for key in data_sync:
        try:dataout[key]=data_sync[key][index_sync]
        except: next
    for key in data_gyr:
        try:dataout[key]=data_gyr[key][dataset_gyr]
        except: next
    
    print(dataout)
    
    
    
    
    
   
    
   
                    
    root.destroy()

    


root = tk.Tk()

#root.withdraw()
    
# 
#
filepath=str() 
file_path = filedialog.askopenfilename()
print(file_path)
#==============================================================================

    
if __name__ == "__main__":
    main(file_path) #
    

    
    
        