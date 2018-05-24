import os
import sys
import time
import math
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
import numpy as np
import scipy.io.wavfile, scipy.io


master = Tk()
master.title('Spatialize Music Tracks GUI')
master.geometry('770x600')

filesarea = Canvas(master, width=300, height=550)
filesarea.pack(side=LEFT, fill=Y)
mousearea = Canvas(master, width=505, height=600, bg="grey", bd = 0)
mousearea.pack(side=RIGHT)

# mousearea.create_rectangle(0, 0, 505, 600, outline="blue")
mousearea.create_oval(5,50,505,550)
mousearea.create_line(5, 300, 505, 300)
mousearea.create_line(255, 50, 255, 550)
mousearea.create_oval(230,275,280,325, outline="red")
mousearea.create_line(255, 255, 255, 290, fill="red")
mousearea.create_line(275, 300, 285, 300, fill="red")
mousearea.create_line(225, 300, 235, 300, fill="red")

def motion(event):
	global colorVar, dynamic_entry
	x, y = event.x, event.y
	distance = math.sqrt( ((x - 255) ** 2) + ((y - 300) ** 2))
	if distance < 250 and colorVar.get() != "None":
		# print('{}, {}'.format(x, y))
		dynamic_mouseAreaIcons[int(colorVar.get())].place(x=x-12,y=y-12)

		dynamic_entry[int(colorVar.get())][0].delete(0, END)
		dynamic_entry[int(colorVar.get())][1].delete(0, END)

		dynamic_entry[int(colorVar.get())][0].insert(0, (x - 255)/10)
		dynamic_entry[int(colorVar.get())][1].insert(0, (300 - y)/10)




mousearea.bind('<Button-1>', motion)

# def is_int():
# 	global numoflabels

# 	for x in xrange(1,10):
# 		newlabel = Label(filesarea, text="newlabel")
# 		newradiobutton = Radiobutton(filesarea, text="One", variable=colorVar, value=numoflabels)
# 		newxentry = Entry(filesarea, width=5)
# 		newyentry = Entry(filesarea, width=5)
# 		newzentry = Entry(filesarea, width=5)
# 		dynamic_labels.append(newlabel)
# 		dynamic_radio.append(newradiobutton)
# 		dynamic_entry[numoflabels][0] = newxentry
# 		dynamic_entry[numoflabels][1] = newyentry
# 		dynamic_entry[numoflabels][2] = newzentry


# 		newlabel.grid(row=numoflabels, column=0)
# 		newradiobutton.grid(row=numoflabels, column=2)
# 		newxentry.grid(row=numoflabels + 1, column=0)
# 		newyentry.grid(row=numoflabels + 1, column=1)
# 		newzentry.grid(row=numoflabels + 1, column=2)
# 		numoflabels = numoflabels + 2

# 	# try:
# 	# 	testx = int(x.get())
# 	# 	testy = int(y.get())
# 	# 	testz = int(z.get())
# 	# 	callback();
# 	# 	return True
# 	# except:
# 	# 	print("Please only enter integers.")
# 	# 	return False
# # master.create_oval(10, 10, 80, 80, outline="gray", fill="gray", width=2)
def generateOutput():
	print "Insert 3D Audio part here XD"


def resetfile(num):
	global colorVar
	colorVar.set(None)
	dynamic_radio[num].configure(state = DISABLED)
	dynamic_entry[num][0].delete(0, END)
	dynamic_entry[num][1].delete(0, END)
	dynamic_entry[num][2].delete(0, END)
	dynamic_entry[num][0].configure(state = DISABLED)
	dynamic_entry[num][1].configure(state = DISABLED)
	dynamic_entry[num][2].configure(state = DISABLED)

	dynamic_labels[num].config(text="No File")
	dynamic_filebutton[num].configure(text="Add File")
	dynamic_filebutton[num].configure(command=lambda name=num:addfile(name))
	dynamic_mouseAreaIcons[num].destroy()


def addfile(num):
	global dynamic_labels, dynamic_radio, dynamic_entry, dynamic_mouseAreaIcons
	filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
	arr = filename.split("/")
	name1 = arr[len(arr)-1].split(".")
	name = name1[0]
	dynamic_radio[num].configure(state = "normal")
	dynamic_entry[num][0].configure(state = "normal")
	dynamic_entry[num][1].configure(state = "normal")
	dynamic_entry[num][2].configure(state = "normal")
	dynamic_labels[num].config(text=name)
	dynamic_filebutton[num].configure(text="Reset")
	dynamic_filebutton[num].configure(command=lambda name=num:resetfile(name))


	newlabel = Label(mousearea, text=num+1, width=2)
	newlabel.place(x=255 - 12,y=300 - 12)
	dynamic_mouseAreaIcons[num] = newlabel

	dynamic_entry[num][0].insert(0, 0)
	dynamic_entry[num][1].insert(0, 0)
	dynamic_entry[num][2].insert(0, 0)
	print (num)

b = Button(filesarea, text="Generate!", width=10, command=generateOutput)
b.grid(row=0,column=1)

dynamic_labels = []
dynamic_radio = []
dynamic_filebutton = []
dynamic_mouseAreaIcons = [-1] * 10
w, h = 3, 100;
dynamic_entry = [[0 for x in range(w)] for y in range(h)]
colorVar = StringVar()
colorVar.set(None)
print colorVar.get()
wavNum = 0
numoflabels = 1

for x in xrange(0,10):
	newlabel = Label(filesarea, text="No File", width=10)
	newreset = Button(filesarea, text="Add File", command=lambda name=wavNum:addfile(name))
	newradiobutton = Radiobutton(filesarea, text=wavNum+1, variable=colorVar, value=wavNum)
	newradiobutton.configure(state = DISABLED)
	newxentry = Entry(filesarea, width=5)
	newyentry = Entry(filesarea, width=5)
	newzentry = Entry(filesarea, width=5)
	newxentry.configure(state = DISABLED)
	newyentry.configure(state = DISABLED)
	newzentry.configure(state = DISABLED)
	dynamic_labels.append(newlabel)
	dynamic_radio.append(newradiobutton)
	dynamic_filebutton.append(newreset)
	dynamic_entry[wavNum][0] = newxentry
	dynamic_entry[wavNum][1] = newyentry
	dynamic_entry[wavNum][2] = newzentry

	newreset.grid(row=numoflabels, column=0)
	newlabel.grid(row=numoflabels, column=1)
	newradiobutton.grid(row=numoflabels, column=2)
	newxentry.grid(row=numoflabels + 1, column=0)
	newyentry.grid(row=numoflabels + 1, column=1)
	newzentry.grid(row=numoflabels + 1, column=2)
	numoflabels = numoflabels + 2
	wavNum = wavNum + 1

mainloop()
