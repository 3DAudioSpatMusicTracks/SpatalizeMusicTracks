import os
import sys
import time
import pygame
from Tkinter import *
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
import numpy as np
import scipy.io.wavfile, scipy.io

master = Tk()
master.title('Spatialize Music Tracks GUI')
master.geometry('300x200')
master.configure(background='black')

xvar = StringVar()
yvar = StringVar()
zvar = StringVar()
xlabel = Label(master, textvariable=xvar, fg='white', bg='black')
ylabel = Label(master, textvariable=yvar, fg='white', bg='black')
zlabel = Label(master, textvariable=zvar, fg='white', bg='black')
xvar.set("X-Coordinate")
yvar.set("Y-Coordinate")
zvar.set("Z-Coordinate")

x = Entry(master, highlightbackground='black')
y = Entry(master, highlightbackground='black')
z = Entry(master, highlightbackground='black')
x.insert(END, '0')
y.insert(END, '0')
z.insert(END, '0')

xlabel.pack()
x.pack()
ylabel.pack()
y.pack()
zlabel.pack()
z.pack()

x.focus_set()
y.focus_set()
z.focus_set()

def run():
    if len (sys.argv) < 2:
        print ("Usage: %s wavefile" % os.path.basename(sys.argv[0]))
        print ("    Using an example wav file...")
        dirname = os.path.dirname(__file__)
        fname = os.path.join(dirname, "hey.wav")
    else:
        fname = sys.argv[1]

    '''
	#drumsFile = "Drums - Four Lights.wav"
	#rhythmGuitarFile = "Rhythm Guitar - Four Lights.wav"

	# bass = wave.open(bassFile, 'r')
	bassFile = "hey.wav"
	bassRate, bassData = scipy.io.wavfile.read(bassFile)

	# Selecting HRTF for User (Double-Check)
	HRTFToUse = tkFileDialog.askopenfilename()  # Opens Tkinter GUI and File Explorer for selecting .mat file
	hrtf = scipy.io.loadmat(HRTFToUse)          # Opens file at stored path
				                                # open(strip(HRTFToUse))

	#print hrtf
	hrir_l =  hrtf['hrir_l']
	hrir_r = hrtf['hrir_r']
	ITD = hrtf['ITD']

	# 25 locations
	negAzimuths = [-80, -65, -55, -45]
	intervalsOf5 = np.arange(-40,45,5).tolist()
	posAzimuths = [45 , 55 , 65, 80]
	azimuths = negAzimuths + intervalsOf5 + posAzimuths

	# 50 locations
	rangeFrom0to49 = np.arange(0.0,50.0,1.0)
	elevations = -45 + 5.625*rangeFrom0to49
	elevations = elevations.tolist()

	aIndex = 4; # Azimuth Index
	eIndex = 1; # Elevation Index

	# Initializing lists for .WAV input
	wav_left = []
	wav_right = []
	soundToPlay = []

	lft = np.squeeze(hrir_l[aIndex, eIndex, :])
	rgt = np.squeeze(hrir_r[aIndex, eIndex, :])

	delay = ITD[aIndex, eIndex];

	if aIndex < 13:
	    lft = np.transpose(lft).tolist() + np.zeros(np.arange(1,np.absolute(delay),1).shape).tolist()
	    rgt = np.zeros(np.arange(1,np.absolute(delay),1).shape).tolist() + np.transpose(rgt).tolist()
	else:
	    lft = np.zeros(np.arange(1,np.absolute(delay),1).shape).tolist() + np.transpose(lft).tolist()
	    rgt = np.transpose(rgt).tolist() + np.zeros(np.arange(1,np.absolute(delay),1).shape).tolist()
	'''
    sink = SoundSink()
    sink.activate()

    xint = int(x.get())
    yint = int(y.get())
    zint = int(z.get())
    source = SoundSource(position=[xint, yint, zint])
    source.looping = False
    
    data = load_wav_file(fname)
    source.queue(data)

    sink.play(source)

    sink.update()
    time.sleep(2)
    print("done")

def callback():
	testx = int(x.get())
	testy = int(y.get())
	testz = int(z.get())

	if testx > 25 or testx < -25 or testy > 25 or testy < -25 or testz > 25 or testz < -25:
		print("Input out of bound. Please make sure they are less than |25|.")
	else:
		run()

def is_int():
	try:
		testx = int(x.get())
		testy = int(y.get())
		testz = int(z.get())
		callback();
		return True
	except:
		print("Please only enter integers.")
		return False

b = Button(master, text="Play!", width=10, command=is_int, highlightbackground='black')
b.pack()


mainloop()
x = Entry(master, width=50)
x.pack()
y = Entry(master, width=50)
y.pack()
z = Entry(master, width=50)
z.pack()

text = e.get()
def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=LEFT)
    return entry

user = makeentry(parent, "User name:", 10)
password = makeentry(parent, "Password:", 10, show="*")
content = StringVar()
entry = Entry(parent, text=caption, textvariable=content)

text = content.get()
content.set(text)
