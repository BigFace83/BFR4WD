from Tkinter import *
from tkFileDialog import *
from PIL import Image
from PIL import ImageTk
import BFR4WDserialGUI
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
        # Draw Map button
        ##################################################################
        self.Draw = Button(self, text="Draw Map")
        self.Draw.bind('<Button-1>', self.DrawMap)
        self.Draw.grid(row = 2, column = 4)

        ##################################################################
        # Change Map button
        ##################################################################
        self.Change = Button(self, text="Change")
        self.Change.bind('<Button-1>', self.ChangeMap)
        self.Change.grid(row = 3, column = 4)


    def NewMap(self,event):
        MapHeight = 100
        MapWidth = 100
        self.MapArray = np.zeros((MapHeight,MapWidth,1), np.float32)
        self.MapArray[:, 0] =  0.0
        self.MapArray[:, 10]  =  0.1
        self.MapArray[:, 20]  =  0.2
        self.MapArray[:, 30]  =  0.3
        self.MapArray[:, 40] =  0.4
        self.MapArray[:, 50]  =  0.5
        self.MapArray[:, 60]  =  0.6
        self.MapArray[:, 70]  =  0.7
        self.MapArray[:, 80]  =  0.8
        self.MapArray[:, 90]  =  0.9
        self.MapArray[:, 99]  =  1
        print "New Map Created"

    def ChangeMap(self,event):
 
        self.MapArray[:, 0] =  1
        self.MapArray[:, 10]  =  0.9
        self.MapArray[:, 20]  =  0.8
        self.MapArray[:, 30]  =  0.7
        self.MapArray[:, 40] =  0.6
        self.MapArray[:, 50]  =  0.5
        self.MapArray[:, 60]  =  0.4
        self.MapArray[:, 70]  =  0.3
        self.MapArray[:, 80]  =  0.2
        self.MapArray[:, 90]  =  0.1
        self.MapArray[:, 99]  =  0
        print "Map Changed"
 

    def DrawMap(self,event):

        print "Drawing Map"
        Map = np.copy(self.MapArray)
        for x in np.nditer(Map , op_flags=['readwrite']): #Loop through entire array
            x[...] = 255-(x* 255) #Convert from a float array (0 to 1) to a grayscale image (0-255)
        

        Map  = Map.astype(np.uint8) #Make array and array of integers

        self.MapImage = cv2.cvtColor(Map ,cv2.COLOR_GRAY2RGB) #Convert to RGB before adding coloured objects
        #cv2.circle(self.MapImage, (50, 50), 20, (0,0,255)) #draw a circle

        self.MapImage = Image.fromarray(self.MapImage)
        self.MapImage = self.MapImage.resize((600, 600))
	self.MapImage = ImageTk.PhotoImage(self.MapImage)
        self.MapCanvas .create_image(0,0, anchor=NW, image=self.MapImage)




root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
