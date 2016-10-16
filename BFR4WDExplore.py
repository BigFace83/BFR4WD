import BFR4WDserialport
import math

xrobot = 0
yrobot = 0
########################################################################################
#
# writetofile
#
########################################################################################
def writetofile(filename, dataarray):
        datastring  =  ','.join([str(x) for x in dataarray])
        filename.write(datastring + '\n')

########################################################################################
#
# Initialise robot
#
########################################################################################
def Initialise(wheelSpeed, headSpeed):

    returned = BFR4WDserialport.sendcommand("S1 V1") #Servo power on
    returned = BFR4WDserialport.sendcommand("S2 V" + str(wheelSpeed))
    returned = BFR4WDserialport.sendcommand("S3 V" + str(headSpeed))

########################################################################################
#
# SonarSweep
#
########################################################################################
def SonarSweep(startAngle, endAngle, stepSize, tilt, filename):

    Heading = BFR4WDserialport.sendcommand("G8") #get robot heading
    for x in range(startAngle, endAngle, stepSize):
        string = "H1 P"+ str(x) + "T"+ str(tilt) #Form string for head move command
        returned = BFR4WDserialport.sendcommand(string) #move head
        sonar = int(BFR4WDserialport.sendcommand("G5")) #get sonar reading
        thetaP = int(Heading) + x #calculate bearing of sonar reading
        thetaT = tilt
        data = [xrobot, yrobot, thetaP, thetaT, sonar] #form data list
        print data
        writetofile(filename,data) #write data list to file
        



########################################################################################
#
# Main
#
########################################################################################

f = open('RawMapData.txt', 'w') #Open a file
Initialise(10,10)
Heading = BFR4WDserialport.sendcommand("G8") #get initial robot heading

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W1 D50") #Forward 50cm
FLdistance = BFR4WDserialport.sendcommand("G1")
RLdistance = BFR4WDserialport.sendcommand("G2")
FRdistance = BFR4WDserialport.sendcommand("G3")
RRdistance = BFR4WDserialport.sendcommand("G4")
averageddistance = (int(FLdistance) + int(RLdistance) + int(FRdistance) + int(RRdistance))/4
Headingrads = math.radians(float(Heading))
xrobot = xrobot + int(math.sin(Headingrads) * averageddistance)
yrobot = yrobot + int(math.cos(Headingrads) * averageddistance) #calculate new robot x and y coordinates


SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W3 D90") #Turn 90

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W1 D50") #Forward 50cm
FLdistance = BFR4WDserialport.sendcommand("G1")
RLdistance = BFR4WDserialport.sendcommand("G2")
FRdistance = BFR4WDserialport.sendcommand("G3")
RRdistance = BFR4WDserialport.sendcommand("G4")
averageddistance = (int(FLdistance) + int(RLdistance) + int(FRdistance) + int(RRdistance))/4
Headingrads = math.radians(float(Heading))
xrobot = xrobot + int(math.sin(Headingrads) * averageddistance)
yrobot = yrobot + int(math.cos(Headingrads) * averageddistance) #calculate new robot x and y coordinates

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W3 D90") #Turn 90

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W1 D50") #Forward 50cm
FLdistance = BFR4WDserialport.sendcommand("G1")
RLdistance = BFR4WDserialport.sendcommand("G2")
FRdistance = BFR4WDserialport.sendcommand("G3")
RRdistance = BFR4WDserialport.sendcommand("G4")
averageddistance = (int(FLdistance) + int(RLdistance) + int(FRdistance) + int(RRdistance))/4
Headingrads = math.radians(float(Heading))
xrobot = xrobot + int(math.sin(Headingrads) * averageddistance)
yrobot = yrobot + int(math.cos(Headingrads) * averageddistance) #calculate new robot x and y coordinates

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W3 D90") #Turn 90

SonarArray = SonarSweep(-60, 60, 10, 0,f)

returned = BFR4WDserialport.sendcommand("W1 D50") #Forward 50cm
FLdistance = BFR4WDserialport.sendcommand("G1")
RLdistance = BFR4WDserialport.sendcommand("G2")
FRdistance = BFR4WDserialport.sendcommand("G3")
RRdistance = BFR4WDserialport.sendcommand("G4")
averageddistance = (int(FLdistance) + int(RLdistance) + int(FRdistance) + int(RRdistance))/4
Headingrads = math.radians(float(Heading))
xrobot = xrobot + int(math.sin(Headingrads) * averageddistance)
yrobot = yrobot + int(math.cos(Headingrads) * averageddistance) #calculate new robot x and y coordinates

SonarArray = SonarSweep(-60, 60, 10, 0,f)





f.close()
returned = BFR4WDserialport.sendcommand("S1 V0") #Servo power off

'''
#Read from file
f = open('RawMapData.txt', 'r')
print 'Reading file'
for line in f:
    string = line.strip().split(',')
    data = [int(i) for i in string]
    print data
 
f.close()
'''

