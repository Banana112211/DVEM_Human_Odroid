#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import writecsv2
import time
import traceback
#Synchronisationsdatei fuer Odroid1 und Odroid2: Systemzeiten werden uebergeben und abgespeichert. (Postprocessing: Delta berechnen)

def client_receive(port=55606,ip='192.168.0.1',name="Syn_O1_O2"):
    # IP und Port als Angabe; name=Probandenname als uebergabeparameter
    file_name=name+"_sync"
    keys=["Odroid2_time","Odorid_2_192.168.0.2_unixtime","Odorid_1_192.168.0.1_unixtime"]
    s_data=dict([(key, []) for key in keys])
    writecsv2.writedatacsv(file_name,s_data,0)
    
    #Write_Logfile.logfile_schreiben("Odroid2_time,Odorid_2_192.168.0.2_unixtime,Odorid_1_192.168.0.1_unixtime",file_name) #oberste Line als ueberschriften
    print "client is online"#rueckgabe bei erfolg
    #f=open(file_name+'log.txt','w')

    #Socketaufbau UDP
    try:
        while True:
            try:
                start=time.time()
                s_data=dict([(key, []) for key in keys])
                s = socket.socket()   
                s.connect((ip, port))# IP, PORT
                #print(str(s.recv(1024)))
                
                s_data[keys[0]].append(time.asctime())
                s_data[keys[1]].append(time.time())
                s_data[keys[2]].append(s.recv(2028))
                writecsv2.writedatacsv(file_name,s_data,1)
                            
                
                #message=s_data#str(str(e[0])+","+str(e[1])+","+str(e[2])+","+str(nr)+","+str(now)) #the whole contain must converted to a string!

                wait=0.05-(time.time()-start)        
                #print(s_data)#message)
               
                time.sleep(abs(wait))
        
                
                
        
        
        
        
                #Write_Logfile.logfile_schreiben(str(time.asctime())+","+str(time.time())+","+str(s.recv(2028)),file_name)#Parameteruebergabe. schreiben der Systemzeiten in Log-File
                s.close()# Close the socket when done
            except KeyboardInterrupt:
                s.close()
                break
            
            except Exception as e:
                #traceback.print_exc(file=f)
                #f.close

                #print(fail)
                s.close()
                break
            
    except Exception as e:
            traceback.print_exc(file=f)
            #f.close         
            #print(fail)
            s.close()
            
    finally:
            print('end sync ',s_data,wait)
            s.close()
            
if __name__=="__main__":
    client_receive(55606,"192.168.0.1",name='test')
