from Tkinter import *
import BFR4WDserialGUI



class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):

        self.commandEntry= Entry(self)
        self.commandEntry.pack(side=LEFT)
        self.commandEntry.bind('<Return>', self.sendCommand)

        self.returnEntry= Entry(self)
        self.returnEntry.pack(side=LEFT)

        self.send = Button(self, text="Send")
        self.send.bind('<Button-1>', self.sendCommand)
        self.send.pack(side=LEFT)

        self.QUIT = Button(self, text="QUIT", fg="red",command=root.destroy)
        self.QUIT.pack(side=BOTTOM)


    def sendCommand(self,event):
        returned = BFR4WDserialGUI.sendcommand(self.commandEntry.get())
        self.returnEntry.delete(0,END)
        self.returnEntry.insert(10,returned) 
        self.commandEntry.delete(0,END)
        
        



root = Tk()
root.title("BFR4WD")
app = Application(master=root)
app.mainloop()
