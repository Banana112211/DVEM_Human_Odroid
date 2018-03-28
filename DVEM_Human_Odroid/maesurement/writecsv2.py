 #-*- coding: utf-8 -*-
""" 
Created on Mon Sep 11 18:08:21 2017

@author: home
""" 

#csv ausgabe
from collections import OrderedDict
import csv
import os
import time
def main():
    '''---nur zu Testzwecken---'''
    name="test" 
    datain={} 
#    gsr=[7,8,9]
#    datain["gsr"]=gsr
    for i in range(2):
        datain.clear()
        hr=[14,15,16]
        rr=[38,39]
        datain["hr"]=hr
        datain["rr"]=rr
#    duration=len(data["hr"])
#    c_rr=len(data["rr"])
#    if c_rr<duration:
#        while c_rr<duration:
#            data["rr"].append(0)
#            c_rr+=1

        writedatacsv(name,datain,1)
        datain.clear()
        gsr=[27,28,29]
        datain["gsr"]=gsr
        writedatacsv(name,datain,0)   
        datain.clear()
        gsr=[21,22,23]
        hr=[17,18,19]
        rr=[30,31]
        datain["hr"]=hr
        datain["rr"]=rr
        datain["gsr"]=gsr
        writedatacsv(name,datain,1)
    datain.clear()
    datain["end"]=[time.time()]
    writedatacsv(name,datain,0)
    datain.clear()
    gsr=[20]
    hr=[10]
    rr=[30]
    datain["hr"]=hr
    datain["rr"]=rr
    datain["gsr"]=gsr
    writedatacsv(name,datain,1)
    
    
    
    

def csvreader(name,append):
    '''---liest CSV file mit Name(name) ein (append==0) oder nur die Keys(append==1)---'''
    
    reader=csv.DictReader(open(name+'.csv', 'r'))
    dread=OrderedDict()
      
    
    #get vorhandene Spalten(not empty)
    if reader.fieldnames:
        try:
            for key in reader.fieldnames:
                dread[key]=[]
    
        except:append=0
    else:append=0
    #vorhandene Spalten mit Daten befüllen
    if append==0:
        for row in reader:
            for key in row:
                try:
                 if not row[key]=="": 
                     dread[key].append(row[key])
                except:next
        
    return dread
    
    



def csvwriter(dread=dict(),f=str(),append=bool()):
    '''überschreibt Daten(dread=dict()) des Files f (!langsamer!) mit (append==0) oder (schneller) hängt diese nur an (append==1)---'''
#            print(for key in dread: dread[key][0])
    line=1
    count=0
    if append==0:
        w = csv.writer(open(f+'.csv', 'w')) 
        w.writerow(dread.keys()) 
    else:
        w = csv.writer(open(f+'.csv', 'a'))
   
    
    #über datenlänge iterieren ´= Zeilenanzahl
    while count<line:
        c=[]
        #über Spalten Zeilen schreiben
        for item in dread:

            if len(dread[item])>line:
                line =len(dread[item])
            try:
                c.append(dread[item][count])                   
            except:
                c.append("")
        count+=1
        w.writerow(c)

def writedatacsv(name=str(),data=dict(),append=bool()):
    '''---liest CSV file mit Name(name) ein und schreibt Daten(data=dict()) komplett neu (!langsamer!) mit (append==0) oder (schneller) hängt diese nur an (append==1)---''' 
    exist=os.path.isfile(name +'.csv')

    if exist == 0:

        writer = csv.writer(open(name+'.csv', 'w'))
        writer.writerow(data.keys())
    
   #---------------------------------------------------------------------------------------     
    dread=csvreader(name,append) 
    if not dread.items():
        append=0
   #überprüfen ob input Dict(data) schon in csv vorhanden falls nicht erstellen, falls ja Daten anhängen
    for key in data:
        if key in dread:
            for d in range(len(data[key])):
                dread[key].append(data[key][d])

        else:
            dread[key]=[]
            dread[key]=data[key]

    #daten schreiben        
    csvwriter(dread,name,append)

if __name__ == '__main__':
    main() 
