from Tkinter import *
import ttk
import tkFileDialog
import subprocess
import string
import os

class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.button_clicks = 0
        self.create_widgets()

    def create_widgets(self):

        global imgLogo
        global imgSrc
        global imgDest
        global imgCrunch
        imgLogo = PhotoImage(file='img/logo.gif')
        imgSrc = PhotoImage(file='img/btnSrc.gif')
        imgDest = PhotoImage(file='img/btnDest.gif')
        imgCrunch = PhotoImage(file='img/btnCrunch.gif')

        self.logo = Canvas(self)
        self.logo.create_image(180, 100, image=imgLogo)
        self.logo['height'] = 200
        self.logo['width'] = 360
        self.logo.grid(row = 0, column = 0)

        #source folder select button
        self.source_button = Label(self)
        self.source_button['image'] = imgSrc
        # self.source_button["text"] = "Source"
        # self.source_button["width"] = "24"
        # self.source_button['command'] = self.source_folder
        self.source_button.bind('<Button-1>', self.source_folder)
        self.source_button.grid(row = 1, column = 0)

        #source folder message
        self.source_text = Text(self, width = 45, height = 1, wrap = WORD)
        self.source_text['padx'] = 20
        self.source_text['pady'] = 10
        self.source_text['bg'] = '#ffffff'
        self.source_text['highlightcolor'] = '#ffffff'
        self.source_text.tag_configure('tag-center', justify='center')
        self.source_text.grid(row = 2, column = 0)

        #destination folder select button
        self.destination_button = Label(self)
        self.destination_button['image'] = imgDest
        # self.destination_button["text"] = "Destination"
        # self.destination_button["width"] = "24"
        # self.destination_button['command'] = self.destination_folder
        self.destination_button.bind('<Button-1>', self.destination_folder)
        self.destination_button.grid(row = 3, column = 0)

        #source folder message
        self.destination_text = Text(self, width = 45, height = 1, wrap = WORD)
        self.destination_text['padx'] = 20
        self.destination_text['pady'] = 10
        self.destination_text['bg'] = '#ffffff'
        self.destination_text['highlightcolor'] = '#ffffff'
        self.destination_text.tag_configure('tag-center', justify='center')
        self.destination_text.grid(row = 4, column = 0)

        #crunch button
        self.crunch_button = Label(self)
        self.crunch_button['image'] = imgCrunch
        # self.crunch_button['text'] = 'CRUNCH!'
        # self.crunch_button['width'] = '24'
        # self.crunch_button['command'] = self.crunch
        self.crunch_button.bind('<Button-1>', self.crunch)
        self.crunch_button.grid(row = 5, column = 0)

        #progress message
        self.progress_text = Text(self, width = 45, height = 1, wrap = WORD)
        self.progress_text['padx'] = 20
        self.progress_text['pady'] = 10
        self.progress_text['bg'] = '#ffffff'
        self.progress_text['highlightcolor'] = '#ffffff'
        self.progress_text.tag_configure('tag-center', justify='center')
        self.progress_text.grid(row = 6, column = 0)

    def source_folder(self, event):
        #select source folder
        global inDir
        inDir = tkFileDialog.askdirectory()
        self.source_text.delete(0.0, END)
        self.source_text.insert(0.0, inDir, 'tag-center')

    def destination_folder(self, event):
        #select source folder
        global outDir
        outDir = tkFileDialog.askdirectory()
        self.destination_text.delete(0.0, END)
        self.destination_text.insert(0.0, outDir, 'tag-center')

    def crunch(self, event):
        try:
            inDir
            outDir

        except NameError:
            self.progress_text.delete(0.0, END)
            self.progress_text.insert(0.0, 'No source/destination', 'tag-center')
        else:
            print "defined"
            #crunch some images
            self.progress_text.delete(0.0, END)
            self.progress_text.insert(0.0, 'Crunching jpegs...', 'tag-center')
            self.progress_text.update()
            print('working...')
            jpegs = [f for f in os.listdir(inDir) if f.endswith(('.jpg', '.JPG'))]
            print(jpegs)
            if not jpegs:
                self.progress_text.delete(0.0, END)
                self.progress_text.insert(0.0, 'I only crunch jpegs, none found', 'tag-center')
            else:
                for jpeg in jpegs:
                    print(jpeg)
                    imgIn = inDir.replace(' ', '\ ') + '/' + jpeg.replace(' ', '\ ')
                    if inDir == outDir:
                        imgOut = outDir.replace(' ', '\ ') + '/' + jpeg.replace(' ', '\ ').replace('.jpg', '-imgcrunch.jpg')
                    else:
                        imgOut = outDir.replace(' ', '\ ') + '/' + jpeg.replace(' ', '\ ')
                    sep = '>'
                    t = string.Template('./mozcjpeg -quality 70 $imgIn > $imgOut')
                    s = t.substitute(vars())
                    print(s)
                    subprocess.call([s], shell=True)
                else:
                    self.progress_text.delete(0.0, END)
                    self.progress_text.insert(0.0, 'Done!', 'tag-center')

root = Tk()
root.title('ImgCrunch beta1')
root.geometry('364x500+60+60')

app = Application(root)

root.mainloop()
