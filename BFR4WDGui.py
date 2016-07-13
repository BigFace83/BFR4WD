from Tkinter import *
from PIL import Image
from PIL import ImageTk
import BFR4WDserialGUI
import BFR4WDOpenCVGui



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):

        ##################################################################
        # Robot Move control graphics
        ##################################################################
        self.TurnACWcontrol = Canvas(self, width=200, height=50)
        self.TurnACWcontrol.grid(row = 0, column = 0)
        self.TurnACW = PhotoImage(file='Images/BFR4WDTurnACW.gif')
        self.TurnACWcontrol .create_image(0,0, anchor=NW, image=self.TurnACW)
        self.TurnACWcontrol.bind('<Button-1>', self.TurnACWclick)

        self.FRcontrol = Canvas(self, width=50, height=255)
        self.FRcontrol.grid(row = 0, column = 1)
        self.FRBar= PhotoImage(file='Images/BFR4WDFRBar.gif')
        self.FRcontrol .create_image(0,0, anchor=NW, image=self.FRBar)
        self.FRcontrol.bind('<Button-1>', self.FRclick)

        self.TurnCWcontrol = Canvas(self, width=200, height=50)
        self.TurnCWcontrol.grid(row = 0, column = 2)
        self.TurnCW = PhotoImage(file='Images/BFR4WDTurnCW.gif')
        self.TurnCWcontrol .create_image(0,0, anchor=NW, image=self.TurnCW)
        self.TurnCWcontrol.bind('<Button-1>', self.TurnCWclick)

        
        ##################################################################
        # Head control graphics
        ##################################################################

        self.HeadTiltcontrol = Canvas(self, width=50, height=255)
        self.HeadTiltcontrol.grid(row = 0, column = 3)
        self.HeadTilt = PhotoImage(file='Images/BFR4WDHeadTilt.gif')
        self.HeadTiltcontrol .create_image(0,0, anchor=NW, image=self.HeadTilt)
        self.HeadTiltcontrol.bind('<Button-1>', self.HeadTiltclick)


        self.HeadPancontrol = Canvas(self, width=255, height=50)
        self.HeadPancontrol.grid(row = 0, column = 4)
        self.HeadPan = PhotoImage(file='Images/BFR4WDHeadPan.gif')
        self.HeadPancontrol .create_image(0,0, anchor=NW, image=self.HeadPan)
        self.HeadPancontrol.bind('<Button-1>', self.HeadPanclick)

        self.CamImage = Canvas(self, width=320, height=240,bg = "black")
        self.CamImage.grid(row = 0, column = 5)



        self.commandEntry= Entry(self)
        self.commandEntry.grid(row = 1, column = 0)
        self.commandEntry.bind('<Return>', self.sendCommand)

        self.returnEntry= Entry(self)
        self.returnEntry.grid(row = 1, column = 1,columnspan=2)

        self.send = Button(self, text="Send")
        self.send.bind('<Button-1>', self.sendCommand)
        self.send.grid(row = 2, column = 0)

        self.servoOnbutton = Button(self, text="Servo Power On")
        self.servoOnbutton.bind('<Button-1>', self.servoOn)
        self.servoOnbutton.grid(row = 1, column = 5)

        self.servoOffbutton = Button(self, text="Servo Power Off")
        self.servoOffbutton.bind('<Button-1>', self.servoOff)
        self.servoOffbutton.grid(row = 2, column = 5)

        self.Capturebutton = Button(self, text="Capture", command = self.CaptureImage)
        #self.Capturebutton.bind('<Button-1>', self.CaptureImage)
        self.Capturebutton.grid(row = 3, column = 5)


        self.QUIT = Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row = 3, column = 3)


    def sendCommand(self,event):
        returned = BFR4WDserialGUI.sendcommand(self.commandEntry.get())
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 
        self.commandEntry.delete(0,END)
        
    def FRclick(self,event):
        self.returnEntry.delete(0,END)
        if event.y < 40 and event.y > 10:
            returned = BFR4WDserialGUI.sendcommand('W1D50')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 70 and event.y > 40:
            returned = BFR4WDserialGUI.sendcommand('W1D30')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 100 and event.y > 70:
            returned = BFR4WDserialGUI.sendcommand('W1D10')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)
        if event.y < 130 and event.y > 100:
            returned = BFR4WDserialGUI.sendcommand('W1D5')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)
        if event.y < 160 and event.y > 130:
            returned = BFR4WDserialGUI.sendcommand('W2D5')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)
        if event.y < 190 and event.y > 160:
            returned = BFR4WDserialGUI.sendcommand('W2D10')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 220 and event.y > 190:
            returned = BFR4WDserialGUI.sendcommand('W2D30')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 250 and event.y > 220:
            returned = BFR4WDserialGUI.sendcommand('W2D50')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 

    def TurnACWclick(self,event):
        self.returnEntry.delete(0,END)
        if event.x < 45 and event.x > 10:
            returned = BFR4WDserialGUI.sendcommand('W3D90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 85 and event.x > 45:
            returned = BFR4WDserialGUI.sendcommand('W3D45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 122 and event.x > 85:
            returned = BFR4WDserialGUI.sendcommand('W3D30')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)
        if event.x < 160 and event.x > 122:
            returned = BFR4WDserialGUI.sendcommand('W3D10')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 200 and event.x > 160:
            returned = BFR4WDserialGUI.sendcommand('W3D5')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 

    def TurnCWclick(self,event):
        self.returnEntry.delete(0,END)
        if event.x < 45 and event.x > 10:
            returned = BFR4WDserialGUI.sendcommand('W4D5')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 85 and event.x > 45:
            returned = BFR4WDserialGUI.sendcommand('W4D10')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 122 and event.x > 85:
            returned = BFR4WDserialGUI.sendcommand('W4D30')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)
        if event.x < 160 and event.x > 122:
            returned = BFR4WDserialGUI.sendcommand('W4D45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 200 and event.x > 160:
            returned = BFR4WDserialGUI.sendcommand('W4D90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned)  


    def HeadPanclick(self,event):
        self.returnEntry.delete(0,END)
        if event.x < 40 and event.x > 10:
            returned = BFR4WDserialGUI.sendcommand('H1P-90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 75 and event.x > 40:
            returned = BFR4WDserialGUI.sendcommand('H1P-45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 110 and event.x > 75:
            returned = BFR4WDserialGUI.sendcommand('H1P-20')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 145 and event.x > 110:
            returned = BFR4WDserialGUI.sendcommand('H1P0')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 175 and event.x > 145:
            returned = BFR4WDserialGUI.sendcommand('H1P20')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 210 and event.x > 175:
            returned = BFR4WDserialGUI.sendcommand('H1P45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.x < 250 and event.x > 210:
            returned = BFR4WDserialGUI.sendcommand('H1P90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 

    def HeadTiltclick(self,event):
        self.returnEntry.delete(0,END)
        if event.y < 40 and event.y > 10:
            returned = BFR4WDserialGUI.sendcommand('H1T90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 75 and event.y > 40:
            returned = BFR4WDserialGUI.sendcommand('H1T45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 110 and event.y > 75:
            returned = BFR4WDserialGUI.sendcommand('H1T20')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 145 and event.y > 110:
            returned = BFR4WDserialGUI.sendcommand('H1T0')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 175 and event.y > 145:
            returned = BFR4WDserialGUI.sendcommand('H1T-20')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 210 and event.y > 175:
            returned = BFR4WDserialGUI.sendcommand('H1T-45')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 
        if event.y < 250 and event.y > 210:
            returned = BFR4WDserialGUI.sendcommand('H1T-90')
            self.returnEntry.delete(0,END)
            self.returnEntry.insert(10,returned) 

        
    def servoOn(self,event):
        returned = BFR4WDserialGUI.sendcommand('S1V1')
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 

    def servoOff(self,event):
        returned = BFR4WDserialGUI.sendcommand('S1V0')
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 

    def CaptureImage(self):
        self.OpenCVImage = BFR4WDOpenCVGui.ReturnFrameRGB()
        self.OpenCVImage = Image.fromarray(self.OpenCVImage)
        self.OpenCVImage = self.OpenCVImage.resize((320, 240), Image.ANTIALIAS)
	self.OpenCVImage = ImageTk.PhotoImage(self.OpenCVImage)
        self.CamImage .create_image(0,0, anchor=NW, image=self.OpenCVImage)
        
        


root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
