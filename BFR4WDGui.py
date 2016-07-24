from Tkinter import *
from tkFileDialog import *
from PIL import Image
from PIL import ImageTk
import BFR4WDserialGUI
import BFR4WDOpenCVGui
import math
import time



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.updateInterval = 500
        self.compassAngle = 0
        self.oktoupdatecompass = True
        self.fileName = StringVar()
        self.after(self.updateInterval, self.updateCompass)
        self.after(self.updateInterval, self.updateSonar)
        self.after(self.updateInterval, self.updateIR)

    def createWidgets(self):

        ##################################################################
        # Robot Move control graphics
        ##################################################################
        self.moveControl = Canvas(self, width=305, height=305)
        self.moveControl.grid(row = 0, column = 0, columnspan = 2, rowspan = 2)
        self.moveImg = PhotoImage(file='Images/BFR4WDMove.gif')
        self.moveControl .create_image(0,0, anchor=NW, image=self.moveImg)
        self.moveControl.bind('<Button-1>', self.moveClick)

        
        ##################################################################
        # Head control graphics
        ##################################################################
        self.headControl = Canvas(self, width=305, height=305)
        self.headControl.grid(row = 0, column = 2, columnspan = 2, rowspan = 2)
        self.headImg = PhotoImage(file='Images/BFR4WDHead.gif')
        self.headControl .create_image(0,0, anchor=NW, image=self.headImg)
        self.headControl.bind('<Button-1>', self.headClick)


        ##################################################################
        # Compass turn to heading graphics
        ##################################################################
        self.compassControl = Canvas(self, width=152, height=152)
        self.compassControl.grid(row = 0, column = 4)
        self.compassImg = PhotoImage(file='Images/BFR4WDCompass.gif')
        self.compassControl .create_image(0,0, anchor=NW, image=self.compassImg)
        self.compassControl.create_oval(25, 25, 127, 127, fill="white",outline="white")
        self.compassControl.create_line(76, 76, 76, 25, fill="black", width=3)
        self.compassControl.bind('<B1-Motion>',  self.TurnToHeading)
        self.compassControl.bind(' <ButtonRelease-1>',  self.commandHeading)
       
        
        ##################################################################
        # Sonar graphics
        ##################################################################
        self.sonarCanvas = Canvas(self, width=152, height=152, bg = 'black')
        self.sonarCanvas.grid(row = 1, column = 4)

        ##################################################################
        # IR graphics
        ##################################################################
        self.irCanvas = Canvas(self, width=152, height=152, bg = 'black')
        self.irCanvas.grid(row = 0, column = 5)



        self.CamImage = Canvas(self, width=320, height=240,bg = "black")
        self.CamImage.grid(row = 3, column = 0, rowspan = 3)

        self.commandEntry= Entry(self)
        self.commandEntry.grid(row = 2, column = 0)
        self.commandEntry.bind('<Return>', self.sendCommand)

        self.returnEntry= Entry(self)
        self.returnEntry.grid(row = 2, column = 2)

        self.send = Button(self, text="Send")
        self.send.bind('<Button-1>', self.sendCommand)
        self.send.grid(row = 2, column = 1)

        self.servoOnbutton = Button(self, text="Servo Power On")
        self.servoOnbutton.bind('<Button-1>', self.servoOn)
        self.servoOnbutton.grid(row = 1, column = 5)

        self.servoOffbutton = Button(self, text="Servo Power Off")
        self.servoOffbutton.bind('<Button-1>', self.servoOff)
        self.servoOffbutton.grid(row = 2, column = 5)

        self.Capturebutton = Button(self, text="Capture", command = self.CaptureImage)
        self.Capturebutton.grid(row = 3, column = 5)

        ##################################################################
        # BFRCode file handling
        ##################################################################

        self.loadfileButton = Button(self, text="Load File")
        self.loadfileButton.grid(row = 3, column = 2)
        self.loadfileButton.bind('<Button-1>', self.loadFile)

        self.fileEntry= Entry(self)
        self.fileEntry.grid(row = 4, column = 2)

        self.runfileButton = Button(self, text="Run File", command = self.runFile)
        self.runfileButton.grid(row = 5, column = 2)


        self.QUIT = Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.grid(row = 3, column = 3)


    def sendCommand(self,event):
        returned = BFR4WDserialGUI.sendcommand(self.commandEntry.get())
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 
        self.commandEntry.delete(0,END)
        

    ##################################################################
    # Move Bar clicked event
    ##################################################################
    def moveClick(self,event):
        self.returnEntry.delete(0,END)
        # Speed select bar clicked
        if event.y > 10 and event.y < 40:
            if event.x >= 5 and event.x < 30:
                returned = BFR4WDserialGUI.sendcommand('S2V2')
                self.returnEntry.insert(10,returned)
            elif event.x >= 30 and event.x < 55:
                returned = BFR4WDserialGUI.sendcommand('S2V4')
                self.returnEntry.insert(10,returned)
            elif event.x >= 55 and event.x < 79:
                returned = BFR4WDserialGUI.sendcommand('S2V6')
                self.returnEntry.insert(10,returned)
            elif event.x >= 79 and event.x < 104:
                returned = BFR4WDserialGUI.sendcommand('S2V8')
                self.returnEntry.insert(10,returned)
            elif event.x >= 104 and event.x < 126:
                returned = BFR4WDserialGUI.sendcommand('S2V10')
                self.returnEntry.insert(10,returned)
        #Forward bar clicked
        if event.x > 133 and event.x < 170:
            if event.y >= 5 and event.y < 38:
                returned = BFR4WDserialGUI.sendcommand('W1D50')
                self.returnEntry.insert(10,returned)
            if event.y >= 38 and event.y < 70:
                returned = BFR4WDserialGUI.sendcommand('W1D30')
                self.returnEntry.insert(10,returned)
            if event.y >= 70 and event.y < 102:
                returned = BFR4WDserialGUI.sendcommand('W1D10')
                self.returnEntry.insert(10,returned)
            if event.y >= 102 and event.y < 133:
                returned = BFR4WDserialGUI.sendcommand('W1D5')
                self.returnEntry.insert(10,returned)
        #Reverse bar clicked
            if event.y >= 170 and event.y < 204:
                returned = BFR4WDserialGUI.sendcommand('W2D5')
                self.returnEntry.insert(10,returned)
            if event.y >= 204 and event.y < 235:
                returned = BFR4WDserialGUI.sendcommand('W2D10')
                self.returnEntry.insert(10,returned)
            if event.y >= 235 and event.y < 268:
                returned = BFR4WDserialGUI.sendcommand('W2D30')
                self.returnEntry.insert(10,returned)
            if event.y >= 268 and event.y < 300:
                returned = BFR4WDserialGUI.sendcommand('W2D50')
                self.returnEntry.insert(10,returned)
        #Turn ACW bar clicked
        if event.y > 134 and event.y < 172:
            if event.x >= 5 and event.x < 38:
                returned = BFR4WDserialGUI.sendcommand('W3D120')
                self.returnEntry.insert(10,returned)
            if event.x >= 38 and event.x < 70:
                returned = BFR4WDserialGUI.sendcommand('W3D90')
                self.returnEntry.insert(10,returned)
            if event.x >= 70 and event.x < 102:
                returned = BFR4WDserialGUI.sendcommand('W3D45')
                self.returnEntry.insert(10,returned)
            if event.x >= 102 and event.x < 133:
                returned = BFR4WDserialGUI.sendcommand('W3D30')
                self.returnEntry.insert(10,returned)
        #Turn CW bar clicked
            if event.x >= 170 and event.x < 204:
                returned = BFR4WDserialGUI.sendcommand('W4D30')
                self.returnEntry.insert(10,returned)
            if event.x >= 204 and event.x < 235:
                returned = BFR4WDserialGUI.sendcommand('W4D45')
                self.returnEntry.insert(10,returned)
            if event.x >= 235 and event.x < 268:
                returned = BFR4WDserialGUI.sendcommand('W4D90')
                self.returnEntry.insert(10,returned)
            if event.x >= 268 and event.x < 300:
                returned = BFR4WDserialGUI.sendcommand('W4D120')
                self.returnEntry.insert(10,returned)

            
                
       
    ##################################################################
    # Head move bar clicked event
    ##################################################################
    def headClick(self,event):
        self.returnEntry.delete(0,END)
        # Speed select bar clicked
        if event.y > 10 and event.y < 40:
            if event.x >= 5 and event.x < 30:
                returned = BFR4WDserialGUI.sendcommand('S3V2')
                self.returnEntry.insert(10,returned)
            elif event.x >= 30 and event.x < 55:
                returned = BFR4WDserialGUI.sendcommand('S3V4')
                self.returnEntry.insert(10,returned)
            elif event.x >= 55 and event.x < 79:
                returned = BFR4WDserialGUI.sendcommand('S3V6')
                self.returnEntry.insert(10,returned)
            elif event.x >= 79 and event.x < 104:
                returned = BFR4WDserialGUI.sendcommand('S3V8')
                self.returnEntry.insert(10,returned)
            elif event.x >= 104 and event.x < 126:
                returned = BFR4WDserialGUI.sendcommand('S3V10')
                self.returnEntry.insert(10,returned)
        #Head tilt up clicked
        if event.x > 133 and event.x < 170:
            if event.y >= 5 and event.y < 38:
                returned = BFR4WDserialGUI.sendcommand('H1T75')
                self.returnEntry.insert(10,returned)
            if event.y >= 38 and event.y < 70:
                returned = BFR4WDserialGUI.sendcommand('H1T50')
                self.returnEntry.insert(10,returned)
            if event.y >= 70 and event.y < 102:
                returned = BFR4WDserialGUI.sendcommand('H1T25')
                self.returnEntry.insert(10,returned)
            if event.y >= 102 and event.y < 133:
                returned = BFR4WDserialGUI.sendcommand('H1T10')
                self.returnEntry.insert(10,returned)
        #Centralise head pan and tilt if central section is clicked 
            if event.y >= 133 and event.y < 170:
                returned = BFR4WDserialGUI.sendcommand('H1T0P0')
                self.returnEntry.insert(10,returned)
        #Head tilt down clicked
            if event.y >= 170 and event.y < 204:
                returned = BFR4WDserialGUI.sendcommand('H1T-10')
                self.returnEntry.insert(10,returned)
            if event.y >= 204 and event.y < 235:
                returned = BFR4WDserialGUI.sendcommand('H1T-25')
                self.returnEntry.insert(10,returned)
            if event.y >= 235 and event.y < 268:
                returned = BFR4WDserialGUI.sendcommand('H1T-50')
                self.returnEntry.insert(10,returned)
            if event.y >= 268 and event.y < 300:
                returned = BFR4WDserialGUI.sendcommand('H1T-75')
                self.returnEntry.insert(10,returned)
        #Head pan ACW clicked
        if event.y > 134 and event.y < 172:
            if event.x >= 5 and event.x < 38:
                returned = BFR4WDserialGUI.sendcommand('H1P-75')
                self.returnEntry.insert(10,returned)
            if event.x >= 38 and event.x < 70:
                returned = BFR4WDserialGUI.sendcommand('H1P-50')
                self.returnEntry.insert(10,returned)
            if event.x >= 70 and event.x < 102:
                returned = BFR4WDserialGUI.sendcommand('H1P-25')
                self.returnEntry.insert(10,returned)
            if event.x >= 102 and event.x < 133:
                returned = BFR4WDserialGUI.sendcommand('H1P-10')
                self.returnEntry.insert(10,returned)
        #Head pan CW clicked
            if event.x >= 170 and event.x < 204:
                returned = BFR4WDserialGUI.sendcommand('H1P10')
                self.returnEntry.insert(10,returned)
            if event.x >= 204 and event.x < 235:
                returned = BFR4WDserialGUI.sendcommand('H1P25')
                self.returnEntry.insert(10,returned)
            if event.x >= 235 and event.x < 268:
                returned = BFR4WDserialGUI.sendcommand('H1P50')
                self.returnEntry.insert(10,returned)
            if event.x >= 268 and event.x < 300:
                returned = BFR4WDserialGUI.sendcommand('H1P75')
                self.returnEntry.insert(10,returned)



    def TurnToHeading(self,event):
         
        self.oktoupdatecompass = False #inhibit drawing actual value whilst selecting new
        self.compassControl.create_oval(25, 25, 127, 127, fill="white",outline="white")
        anglerad = math.atan2(event.x-76,76-event.y)
        self.compassAngle = math.degrees(anglerad)
        if self.compassAngle< 0:
            self.compassAngle = 360 + self.compassAngle

        circlex = 76 + (math.sin(anglerad)*51)
        circley = 76 - (math.cos(anglerad)*51)
        
        self.compassControl.create_line(76, 76, circlex, circley, fill="black", width=3)

    def commandHeading(self,event):
        returned = BFR4WDserialGUI.sendcommand('W7V' + str(self.compassAngle))
        self.returnEntry.insert(10,returned)
        self.oktoupdatecompass = True
        self.after(self.updateInterval, self.updateCompass) #restart drawing actual value after new angle is sent



        
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
        

    def updateCompass(self):
        self.compassControl.create_oval(25, 25, 127, 127, fill="white",outline="white")
        returned = BFR4WDserialGUI.sendcommand('G8')
        anglerad = math.radians(float(returned))
        circlex = 76 + (math.sin(anglerad)*51)
        circley = 76 - (math.cos(anglerad)*51)
        self.compassControl.create_line(76, 76, circlex, circley, fill="red", width=3)
        if self.oktoupdatecompass:
            self.after(self.updateInterval, self.updateCompass)

    def updateSonar(self):
        returned = BFR4WDserialGUI.sendcommand('G5')
        self.sonarCanvas.delete("all")
        y = 152-(int(returned)/1.5)
        if int(returned) <= 40:
            colour = 'red'
        elif int(returned) > 40 and int(returned) <= 80:
            colour = 'orange'
        else:
            colour = 'green'
        self.sonarCanvas.create_polygon((76,152),(56,y),(96,y), fill=colour)
        self.sonarCanvas.create_text(20,132,fill = colour,text = str(returned) + 'cm')
        self.after(self.updateInterval, self.updateSonar)

    def updateIR(self):
        LeftIR = BFR4WDserialGUI.sendcommand('G6')
        RightIR = BFR4WDserialGUI.sendcommand('G7')
        self.irCanvas.delete("all")
        YLeft = (int(LeftIR)/4)
        YRight = (int(RightIR)/4)
       
        self.irCanvas.create_rectangle(36,152,56,YLeft, fill='red')
        self.irCanvas.create_rectangle(96,152,116,YRight, fill='red')
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10, 'Left = ' + str(LeftIR) + ' Right = ' + str(RightIR)) 
        self.after(self.updateInterval, self.updateIR)

    def loadFile(self,event):
        self.fileName = askopenfilename(filetypes=[('BFRCode files', '*.bfr')])
        self.fileEntry.delete(0,END)
        self.fileEntry.insert(10,self.fileName) 

    def runFile(self):
        if self.fileName is not None:
            RunFileSequence(self.fileName)
        
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
                BFR4WDOpenCVGui.SaveFrame(filename)
                imagecounter += 1

            else:
                returned =  BFR4WDserialGUI.sendcommand(command) 
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
            


root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
