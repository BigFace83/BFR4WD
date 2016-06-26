#!/usr/bin/python

########################################################################################
#
# |B|I|G| |F|A|C|E| |R|O|B|O|T|I|C|S|
#
# A Python script for controlling the BFR4WD mobile robot
#
#
# Author : Peter Neal
#
# Date : 12 SEPT 2015
# Last Update : 12 SEPT 2015
#
########################################################################################

import time
import BFR4WDserialport
import numpy
import math
import BFR4WDOpenCV
from colorama import init,Fore
init(autoreset=True)


        
########################################################################################
#
# Opencv threshold values
#
########################################################################################

YELLOWOBJECTS = [15,90,90,40,255,255]
BLUEOBJECTS = [100,145,130,130,255,255]
ORANGEOBJECTS = [5,170,170,15,255,255]
GREENOBJECTS = [40,60,60,100,200,230]

########################################################################################
#
# Robot control variables
#
########################################################################################



########################################################################################
#
# Get encoder counts
#
########################################################################################
def GetEncCounts():

    EncArray = []
    EncArray.append(int(BFR4WDserialport.sendcommand("G1")))
    EncArray.append(int(BFR4WDserialport.sendcommand("G2")))
    EncArray.append(int(BFR4WDserialport.sendcommand("G3")))
    EncArray.append(int(BFR4WDserialport.sendcommand("G4")))
 
    return EncArray

########################################################################################
#
# GetIR
#
########################################################################################
def GetIR():

    IRArray = []
    IRArray.append(int(BFR4WDserialport.sendcommand("G6")))
    IRArray.append(int(BFR4WDserialport.sendcommand("G7")))
    return IRArray


########################################################################################
#
# SonarScan
#
########################################################################################
def SonarScan():

    SonarArray = []
    returned = BFR4WDserialport.sendcommand("S2 V10")
   
    for x in range(-80,80,5):
        string = "H1 P"+ str(x) + " T0"
        returned = BFR4WDserialport.sendcommand(string)
        sonar = int(BFR4WDserialport.sendcommand("G5"))
        SonarArray.append(sonar)
   
    return SonarArray


########################################################################################
#
# Run Sequence
#
########################################################################################
def RunSequence(seq):

    imagecounter = 0

    for x in seq:
        print x
        if 'IMGSAVE' in x:
            time.sleep(0.2) #Let image settle
            filename = 'Images/'+str(imagecounter)+".png"
            print "File Name:  ", filename
            BFR4WDOpenCV.SaveFrame(filename)
            imagecounter += 1
        else:
            returned = BFR4WDserialport.sendcommand(x) 
            if 'E0' in returned:
                print "Command Complete"
            elif 'E1' in returned:
                print "Invalid command"
                return
            elif 'E2' in returned:
                print "Obstacle: Sonar"
                return
            elif 'E3' in returned:
                print "Obstacle: Left IR"
                return
            elif 'E4' in returned:
                print "Obstacle: Right IR"
                return

########################################################################################
#
# Run File Sequence
#
########################################################################################
def RunFileSequence(filename):

    f = open(filename, 'r')
    imagecounter = 0


    for x in f:
        
        command = x.split("#")[0].rstrip('\n') #remove comments and newline characters
        if not command: #do nothing if remaining string is empty
            pass
        else:
            print command
       
            if 'IMGSAVE' in x:
                time.sleep(0.3) #Let image settle
                filename = 'Images/'+str(imagecounter)+".png"
                print "File Name:  ", filename
                BFR4WDOpenCV.SaveFrame(filename)
                imagecounter += 1

            else:
                returned = BFR4WDserialport.sendcommand(command) 
                if 'E0' in returned:
                    print "Command Complete"
                elif 'E1' in returned:
                    print "Invalid command"
                    return
                elif 'E2' in returned:
                    print "Obstacle: Sonar"
                    return
                elif 'E3' in returned:
                    print "Obstacle: Left IR"
                    return
                elif 'E4' in returned:
                    print "Obstacle: Right IR"
                    return
            



########################################################################################
#
# Manual mode
#
########################################################################################
def manualmode():

    while True:
        command = raw_input("Command: ")
        if 'exit' in command:
            break
        returned = BFR4WDserialport.sendcommand(command) 
        if  'E0' in returned:
            print "Command Complete"
        elif  'E1' in returned:
            print "Invalid Command"
        else:
            print returned
        



########################################################################################
#
# Main
#
########################################################################################

while True:
    print "Mode options: M = manual mode.  A = Move and Look.  B = Square. S = Sonar Scan. T = Test"
    mode = raw_input("Mode:  ")
    if mode == 'M':
        manualmode()
    elif mode == 'A':
        time.sleep(3)
        RunSequence(["S1 V8","S2 V4","H1 P0 T0", "W1 D300", "H1 P-80", "W1 D300", "W2 D300","S1 V25","H1 P0","W1 D400"])
    elif mode == 'B':
        time.sleep(3)
        RunSequence(["S1 V15","S2 V3", "W1 D200","W3 D160","W1 D200","W3 D160","W1 D200","W3 D160","W1 D200","W3 D160"])
    elif mode == 'S':
        SonarArray = SonarScan()
        print SonarArray
    elif mode == 'T':
        RunFileSequence('BFRCode/Testfile')
        






BFR4WDserialport.closeserial()  





