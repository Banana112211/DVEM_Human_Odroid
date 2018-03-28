# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:12:05 2017

@author: home
"""
import writecsv2
import hrv

def main(name, test=0):
    """Variablen anlegen"""
    
    rri=[] #rr intervall
    rri_av=[] #rr intervall for  av
    av=[11,15,21]#werte for moving hrv analysis
    dataout=dict()#ausgabe dict
    t=0
    dataout["01_time (s)"]=[]#Zeitvariable Puls und GSR
    dataout["time_rr"]=[]##Zeitvariable rr = integrate rr
    dataout["01_time (s)"].append(t)
    dataout["time_rr"].append(t)
    dataout["Hautwiderstand"]=[]
    
    messspannug_max_oszi=5.0 #volt
    aufloesung=128.0 #bit
    
    widestand_spannungsteiler=220000.0 #ohm
    eingangs_spannung=3.3 #volt
    
    """alle daten einlesen"""

    data=writecsv2.csvreader(name,0)
    
    for gsr in data["gsr"]:
        t+=1
        """widestandsberechnung aus oszimessung"""
        du_haut=messspannug_max_oszi-float(gsr)*(messspannug_max_oszi/aufloesung)
        r_haut=widestand_spannungsteiler*(eingangs_spannung-du_haut)/du_haut
        dataout["Hautwiderstand"].append(r_haut) 
        """zeit in s schreiben"""                        
        dataout["01_time (s)"].append(t)
    
        
    for i in range(len(data["rr"])):
        rri.append(int(data["rr"][i]))#rr daten einlesen
        t=dataout["time_rr"][i]+int(data["rr"][i])/1000 #integrate over rri
              
        dataout["time_rr"].append(t)
        for l in av:#schleife averages
            if i<(len(data["rr"])-l):
                
                rri_av.clear()
                for x in range(l):
                    rri_av.append(int(data["rr"][i+x]))#array zur uebergabe befuellen
                    
                data_hrv=hrv.classical.time_domain(rri_av)#eigentliche hrv analyse
                """VVV---daten ins dict schieben---VVV"""    
                for key in data_hrv:
                    key_out=key+"_"+str(l)
                    if key_out in dataout:
                            dataout[key_out].append(data_hrv[key])
            
                    else:
                        zeros=int((l-1)/2)
                        dataout[key_out]=[]
                        for y in range(zeros):
                            dataout[key_out].append(0)
                        dataout[key_out].append(data_hrv[key])
        """-------------falls test 1 Blocklaenge stresstest schreiben-----------"""              
        if test==1:
            dataout["Block_length"]=[]
            dataout["Block_length"].append(180)
            dataout["Block_length"].append(180)
            dataout["Block_length"].append(180)
            dataout["Block_length"].append(12)
        
            
                    
    
    #print(dataout)
    writecsv2.writedatacsv(name,dataout,0)#daten in csv pushen
    
if __name__ == '__main__':
    main() 