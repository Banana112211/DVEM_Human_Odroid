# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 18:08:16 2017

@author: root
"""
import os

def logfile_schreiben(datensatz,name_txtfile):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path+"/"+name_txtfile+".txt", "a") as myfile:
        myfile.write(datensatz+"\n")
