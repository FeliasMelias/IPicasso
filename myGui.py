from tkinter import *
import PIL.Image as Image, PIL.ImageTk as ImageTk
import hopfield


def startProgram(guiData):

    hopfield.main(guiData)


def noisyImageChanged(imagePath, guiData):
    imagePath = r'PicsRausch/'+imagePath
    print(imagePath)
    labelImage1 = guiData[0]
    window = guiData[2]
    load = Image.open(imagePath)
    new_width = 200
    new_height = 200
    load = load.resize((new_width, new_height))
    render = ImageTk.PhotoImage(load)
    labelImage1.config(image=render)
    labelImage1.image = render
    window.update()


def aiImageChanged(image, guiData):
    print("image: "+str(image))
    load = image
    labelImage2 = guiData[1]
    window = guiData[2]
    new_width = 200
    new_height = 200
    load = load.resize((new_width, new_height))
    render = ImageTk.PhotoImage(load)
    labelImage2.config(image=render)
    labelImage2.image = render
    window.update()
#window laden
def startWindow():
    windowWidth = 1280
    windowHeight = 720
    window = Tk()
    window.title("IPicasso")
    canvas = Canvas(window, height=windowHeight, width=windowWidth)
    canvas.pack()

    frameImage1 = Frame(window, bg='blue')
    frameImage1.place(relx=0, rely=0, relwidth=0.3, relheight=1)

    frameSettings = Frame(window, bg='grey')
    frameSettings.place(relx=0.3, rely=0, relwidth=0.4, relheight=1)

    frameImage2 = Frame(window, bg='yellow')
    frameImage2.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)


    #images laden
    load = Image.open(r"pics\1.png")
    new_width = 200
    new_height = 200
    load = load.resize((new_width, new_height))
    render = ImageTk.PhotoImage(load)

    labelImage1 = Label(frameImage1, image=render)
    labelImage1.place(rely=0.3, relx=0.3)
    #setImg1(img1)
    startlabel = Label(frameImage1, text="Das Startbild" ,font=50)
    startlabel.place(rely=0.1, relx=0.3)
    label = Label(frameSettings,text="Settings", bg='grey', font=50)
    label.place(rely=0.1, relx=0.3)
    label = Label(frameImage2, text="Die laufenden Veränderungen", font=50)
    label.place(rely=0.1, relx=0.3)
    labelImage2 = Label(frameImage2, image=render)
    labelImage2.place(rely=0.3, relx=0.3)
    guiData = [labelImage1, labelImage2, window]

    startButton = Button(frameSettings, text="Start", width=10, command=lambda: startProgram(guiData), font=40)
    startButton.place(relx=0.3, rely=0.8, relwidth=0.3)

    window.mainloop()




