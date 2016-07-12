from Tkinter import *
import BFR4WDserialGUI



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):


        self.TurnACWcontrol = Canvas(self, width=200, height=50)
        self.TurnACWcontrol.pack(side=LEFT)
        self.TurnACW = PhotoImage(file='Images/BFR4WDTurnACW.gif')
        self.TurnACWcontrol .create_image(0,0, anchor=NW, image=self.TurnACW)
        self.TurnACWcontrol.bind('<Button-1>', self.TurnACWclick)

        self.FRcontrol = Canvas(self, width=50, height=255)
        self.FRcontrol.pack(side=LEFT)
        self.FRBar= PhotoImage(file='Images/BFR4WDFRBar.gif')
        self.FRcontrol .create_image(0,0, anchor=NW, image=self.FRBar)
        self.FRcontrol.bind('<Button-1>', self.FRclick)

        self.TurnCWcontrol = Canvas(self, width=200, height=50)
        self.TurnCWcontrol.pack(side=LEFT)
        self.TurnCW = PhotoImage(file='Images/BFR4WDTurnCW.gif')
        self.TurnCWcontrol .create_image(0,0, anchor=NW, image=self.TurnCW)
        self.TurnCWcontrol.bind('<Button-1>', self.TurnCWclick)

        

        self.commandEntry= Entry(self)
        self.commandEntry.pack(side=LEFT)
        self.commandEntry.bind('<Return>', self.sendCommand)

        self.returnEntry= Entry(self)
        self.returnEntry.pack(side=LEFT)

        self.send = Button(self, text="Send")
        self.send.bind('<Button-1>', self.sendCommand)
        self.send.pack(side=LEFT)

        self.servoOnbutton = Button(self, text="Servo Power On")
        self.servoOnbutton.bind('<Button-1>', self.servoOn)
        self.servoOnbutton.pack(side=LEFT)

        self.servoOffbutton = Button(self, text="Servo Power Off")
        self.servoOffbutton.bind('<Button-1>', self.servoOff)
        self.servoOffbutton.pack(side=LEFT)

        
       

        self.QUIT = Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.pack(side=BOTTOM)


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

        
    def servoOn(self,event):
        returned = BFR4WDserialGUI.sendcommand('S1V1')
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 

    def servoOff(self,event):
        returned = BFR4WDserialGUI.sendcommand('S1V0')
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 


root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
