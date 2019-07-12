# view
from tkinter import *
from tkinter import ttk
import PIL.Image as Image, PIL.ImageTk as ImageTk
import hopfield
import math

class View(Tk):

    def __init__(self, startProgramm):
        Tk.__init__(self)
        self.callback = startProgramm
        # Fenster
        windowWidth = 1280
        windowHeight = 720
        self.title("IPica")
        canvas = Canvas(self, height=windowHeight, width=windowWidth)
        canvas.pack()
        #frames
        frameImage1 = Frame(master=self, bg='blue')
        frameImage1.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        frameSettings = Frame(master=self, bg='grey')
        frameSettings.place(relx=0.3, rely=0, relwidth=0.4, relheight=1)
        frameImage2 = Frame(master=self, bg='yellow')
        frameImage2.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)

        #styles
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="white")

        # Entries


        # Button
        self.startButton = Button(frameSettings, text="Start", width=10, command=self.callback, font=40)
        self.startButton.place(relx=0.25, rely=0.8, relwidth=0.5)
        # Labels
        # Labels Left
        self.labelOriginalImage = Label(frameImage1, text="Das Startbild", font=50)
        self.labelOriginalImage.place(rely=0.1, relx=0.3)
        self.labelUnterschriftLeft = Label(frameImage1, text="", font=50)
        self.labelUnterschriftLeft.place(rely=0.6, relx=0.3)
        #Labels mid
        self.labelSettings = Label(frameSettings, text="Settings", bg='grey', font=50)
        self.labelSettings.place(rely=0.01, relx=0.3)
        self.labelLearnedExamples = Label(frameSettings, text="Gelernte Beispiele: ", bg='grey', font=50)
        self.labelLearnedExamples.place(rely=0.1, relx=0.3)
        self.labelProgressbar = Label(frameSettings, text="Lerne Muster: ", bg='grey', font=30)
        self.labelProgressbar.place(rely=0.15, relx=0.3)
        self.progressbar = ttk.Progressbar(frameSettings, orient="horizontal",
                                        length=200, mode="determinate")
        self.progressbar["value"] = 0
        self.progressbar.place(rely=0.2, relx=0.3)
        self.labelLearningTime = Label(frameSettings, text="Lernzeit: ", bg='grey', font=30)
        self.labelLearningTime.place(rely=0.25, relx=0.3)

        self.labelTimeNeededForExample = Label(frameSettings, text="Benötigte Rechenzeit für das Beispiel: ", bg='grey', font=30)
        self.labelTimeNeededForExample.place(rely=0.3, relx=0.3)
        self.labelTotalTimeNeeded = Label(frameSettings, text="Benötigte Rechenzeit: ", bg='grey', font=30)
        self.labelTotalTimeNeeded.place(rely=0.35, relx=0.3)

        #Labels Right
        self.labelProgressImage = Label(frameImage2, text="Die laufenden Veränderungen", font=50)
        self.labelProgressImage.place(rely=0.1, relx=0.3)
        self.labelUnterschriftRight = Label(frameImage2, text="", font=50)
        self.labelUnterschriftRight.place(rely=0.6, relx=0.3)

        #Images
        load1= Image.open(r"startImages\image1.jpg")
        load2 = Image.open(r"startImages\image2.jpg")
        new_width = 200
        new_height = 200
        load1 = load1.resize((new_width, new_height))
        load2 = load2.resize((new_width, new_height))
        render1 = ImageTk.PhotoImage(load1)
        render2 = ImageTk.PhotoImage(load2)

        self.labelImageLeft = Label(frameImage1, image=render1)
        self.labelImageLeft.image = render1
        self.labelImageLeft.place(rely=0.3, relx=0.3)
        self.labelImageRight = Label(frameImage2, image=render2)
        self.labelImageRight.image = render2
        self.labelImageRight.place(rely=0.3, relx=0.3)


# controller
class Controller(object):
    def __init__(self):
        self.view = View(self.startProgramm)
        self.view.mainloop()

    def startProgramm(self):
        hopfield.main(self)


    def changeProgressbar(self, value):

        progressbar = self.view.progressbar
        labelProgressbar = self.view.labelProgressbar

        labelProgressbar.config(text="Lerne Muster:: "+str(value)+" %")
        progressbar["value"] = value
        self.view.update()

    def changeLeftImage(self, imagePath, counter):
        '''
        Here we can see the original Image, which is gonna changed by the AI
        :param imagePath: The Path for the noisy Image
        :param counter: the Number of the current noisy Picture
        '''
        #imagePath = r'PicsRausch/' + imagePath

        labelImage = self.view.labelImageLeft
        load = Image.open(imagePath)
        new_width = 200
        new_height = 200
        load = load.resize((new_width, new_height))
        render = ImageTk.PhotoImage(load)
        labelImage.config(image=render)
        labelImage.image = render

        labelUnterschriftLeft = self.view.labelUnterschriftLeft
        labelUnterschriftLeft.config(text="VerauschtesBild Nr."+str(counter))

        self.view.update()



    def changeRightImage(self, image, counter):
        '''
        Here we get the changed Imaged, which is processed by the AI, to see the progress,
        the AI is doing,
        :param image: the changed noisy Picture
        '''
        # Eingabe
        #load2 = Image.open(r"pics\4.png")
        new_width = 200
        new_height = 200
        load2 = image.resize((new_width, new_height))
        render2 = ImageTk.PhotoImage(load2)
        imageLeft = self.view.labelImageRight

        imageLeft.config(image=render2)
        imageLeft.image = render2

        labelUnterschriftRight = self.view.labelUnterschriftRight
        labelUnterschriftRight.config(text="Durchlauf: "+str(counter))

        self.view.update()

    def changeLearningTimeLabel(self, time):

        self.view.labelLearningTime.config(text='Lernzeit: '+str(round(time,  2))+' s')
        self.view.update()
    def changeLearnedExamplesLabel(self, num):

        self.view.labelLearnedExamples.config(text="Gelernte Beispiele: "+str(num))
        self.view.update()
    def changeTimeNeededForExampleLabel(self, time):

        self.view.labelTimeNeededForExample.config(text="Benötigte Rechenzeit für das letzte Beispiel:"+str(round(time,  2))+"s")
        self.view.update()
    def changeTotalTimeNeededLabel(self, time):

        self.view.labelTotalTimeNeeded.config(text="Benötigte Rechenzeit:"+str(round(time,  2))+"s")
        self.view.update()
        # a = eval(self.view.eA.get())
       # b = eval(self.view.eB.get())

        # Verarbeitung
        # ------------------ hier die Verarbeitung programmieren ------------
        #s = a + b
        # -------------------------------------------------------------------

        # Ausgabe

        #self.view.lC.config(text=str(s))

# Hauptprogramm
c = Controller()
