from Tkinter import *
from tkFileDialog import *
from PIL import Image
from PIL import ImageTk
import math
import time
import numpy as np
import cv2



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.MapArray = 0
        self.MapHeight = 100
        self.MapWidth = 100
        self.robotX = int(self.MapWidth/2)
        self.robotY = int(self.MapHeight/2)
        self.cellSizeCm = 10
        self.createWidgets()



    def createWidgets(self):

        ##################################################################
        # Map Canvas
        ##################################################################
        self.MapCanvas = Canvas(self, width=600, height=600)
        self.MapCanvas.grid(row = 0, column = 0, columnspan = 4, rowspan = 4)
        self.NewMap()


        ##################################################################
        # Angle entry box
        ##################################################################
        self.angleEntry= Entry(self)
        self.angleEntry.grid(row =1, column = 5)

        ##################################################################
        # Distance entry box
        ##################################################################
        self.distEntry= Entry(self)
        self.distEntry.grid(row =2, column = 5)

        ##################################################################
        # Cone Angle entry box
        ##################################################################
        self.coneEntry= Entry(self)
        self.coneEntry.grid(row =3, column = 5)


        ##################################################################
        # Plot button
        ##################################################################
        self.Plot = Button(self, text="Plot")
        self.Plot.bind('<Button-1>', self.UpdateMap)
        self.Plot.grid(row = 4, column = 5)



    def NewMap(self):

        self.MapArray = np.zeros((self.MapHeight,self.MapWidth,1), np.float32)
        for x in np.nditer(self.MapArray , op_flags=['readwrite']): #Loop through entire array
            x[...] = 0.5 #Set all values to 0.5
        print "New Map Created"
        self.DrawMap()



    def UpdateMap(self,event):
        self.NewMap()
        heading = int(self.angleEntry.get())
        distance = int(self.distEntry.get())
        coneangle = int(self.coneEntry.get())

        #Find cells in cone
        cellarray = []

        for angle in range((heading-coneangle/2), (heading+coneangle/2), 1):
            anglerad = math.radians(float(angle))
            endX = self.robotX - (math.cos(anglerad)*((distance)/self.cellSizeCm))
            endY = self.robotY + (math.sin(anglerad)*((distance)/self.cellSizeCm))
            cells = raytrace((self.robotX,self.robotY),(int(endX), int(endY)))
            for x in cells:
                match = False
                for y in cellarray: #Check to see if cell reference is already in cellarray
                    if y == x:           #If it is...
                        match = True  #...don't add it to cellarray
                if match is False: #Only add unique cells
                    cellarray.append(x)




        for x in cellarray:
            if (x[0] > 0 and x[0] < self.MapWidth and x[1] > 0 and x[1] < self.MapHeight):
                if self.MapArray[x[0], x[1]]>0.1:
                    self.MapArray[x[0], x[1]] -= 0.1
     


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
        self.MapImage = self.MapImage.resize((600, 600))
	self.MapImage = ImageTk.PhotoImage(self.MapImage)
        self.MapCanvas .create_image(0,0, anchor=NW, image=self.MapImage)



def raytrace(start, end):
 
    cells = []
    # Setup initial conditions
    x0, y0 = start
    x1, y1 = end


    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x = x0
    y = y0
    n = 1 + dx + dy
    if (x1 > x0):
        x_inc = 1
    else:
        x_inc = -1
    if (y1 > y0):
        y_inc = 1
    else:
        y_inc = -1
 
    error = dx - dy
    dx *= 2
    dy *= 2

    for steps in range(n):
        coords = (x,y)
        cells.append(coords)

        if (error > 0):
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx

    return cells




root = Tk()
root.title("Sonar Model")
app = Application(master=root)
app.mainloop()
