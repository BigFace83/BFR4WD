from Tkinter import *
from tkFileDialog import *
from PIL import Image
from PIL import ImageTk
import BFR4WDserialport
import math
import time
import numpy as np
import cv2



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.MapArray = 0
        self.updateInterval = 5
        self.MapHeight = 80
        self.MapWidth = 80
        self.robotX = self.MapWidth/2
        self.robotY = self.MapHeight/2
        self.cellSizeCm = 5
        self.Drawcounter = 0



    def createWidgets(self):

        ##################################################################
        # Map Canvas
        ##################################################################
        self.MapCanvas = Canvas(self, width=600, height=600)
        self.MapCanvas.grid(row = 0, column = 0, columnspan = 3, rowspan = 3)
  

        ##################################################################
        # New Map button
        ##################################################################
        self.New = Button(self, text="New Map")
        self.New.bind('<Button-1>', self.NewMap)
        self.New.grid(row = 1, column = 4)

        ##################################################################
        # Scan button
        ##################################################################
        self.Scan= Button(self, text="Scan",command=self.SingleScan)
        self.Scan.grid(row = 2, column = 4)



    def NewMap(self,event):

        self.MapArray = np.zeros((self.MapHeight,self.MapWidth,1), np.float32)
        print "New Map Created"
        self.DrawMap()

    def SingleScan(self):

        data = SonarSweep(-80,80,10,0)
        for x in range(len(data)):
            anglerad = math.radians(float(data[x][0]))
            yobj = self.robotY - (math.cos(anglerad)*((int(data[x][2]))/self.cellSizeCm))
            xobj = self.robotX - (math.sin(anglerad)*((int(data[x][2]))/self.cellSizeCm))
            if (xobj > 0 and xobj < self.MapWidth and yobj > 0 and yobj < self.MapHeight):
                self.MapArray[xobj,yobj] = 0.5
        self.DrawMap()


 

    #Convert from np array to a displayable image and send to screen
    def DrawMap(self):

        print "Drawing Map"
        Map = np.copy(self.MapArray)
        for x in np.nditer(Map , op_flags=['readwrite']): #Loop through entire array
            x[...] = 255-(x* 255) #Convert from a float array (0 to 1) to a grayscale image (0-255)
        
        Map  = Map.astype(np.uint8) #Make array an array of integers

        self.MapImage = cv2.cvtColor(Map ,cv2.COLOR_GRAY2RGB) #Convert to RGB before adding coloured objects
        cv2.circle(self.MapImage, (self.robotX, self.robotY), 1, (255,0,0),-1) #draw a circle at centre point of object
        self.MapImage = Image.fromarray(self.MapImage)
        self.MapImage = self.MapImage.resize((200, 200))
	self.MapImage = ImageTk.PhotoImage(self.MapImage)
        self.MapCanvas .create_image(0,0, anchor=NW, image=self.MapImage)



########################################################################################
#
# SonarSweep
#
########################################################################################
def SonarSweep(startAngle, endAngle, stepSize, tilt):

    dataarray = []
    returned= BFR4WDserialport.sendcommand('S1V1') #servo power on
    returned= BFR4WDserialport.sendcommand('S3V10') #Head speed

    for x in range(startAngle, endAngle, stepSize):
        Heading = BFR4WDserialport.sendcommand("G8") #get robot heading
        string = "H1 P"+ str(x) + "T"+ str(tilt) #Form string for head move command
        returned = BFR4WDserialport.sendcommand(string) #move head
        sonar = int(BFR4WDserialport.sendcommand("G5")) #get sonar reading
        thetaP = int(Heading) + x #calculate bearing of sonar reading using compass data and servo angle
        thetaT = tilt
        data = [thetaP, thetaT, sonar] #form data list
        dataarray.append(data)
        
        
    returned= BFR4WDserialport.sendcommand('S1V0') #servo power off
    return dataarray
        

########################################################################################
#
# Get IR
#
########################################################################################
def GetIR():

    dataarray = []
    Heading = BFR4WDserialport.sendcommand("G8") #get robot heading

    Left= int(BFR4WDserialport.sendcommand("G6")) #get left IR reading
    
    








root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
