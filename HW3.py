import os
import sys
import time
from Tkinter import *
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file

master = Tk()

e = Entry(master)
y = Entry(master)
z = Entry(master)
e.pack()
y.pack()
z.pack()

e.focus_set()
y.focus_set()
z.focus_set()

def callback():
    print e.get()
    print y.get()
    print z.get()
    def run():
	    if len (sys.argv) < 2:
	        print ("Usage: %s wavefile" % os.path.basename(sys.argv[0]))
	        print ("    Using an example wav file...")
	        dirname = os.path.dirname(__file__)
	        fname = os.path.join(dirname, "hey.wav")
	    else:
	        fname = sys.argv[1]

	    sink = SoundSink()
	    sink.activate()

	    source = SoundSource(position=[10, 0, 0])
	    source.looping = False

	    data = load_wav_file(fname)
	    source.queue(data)

	    sink.play(source)
	    print("done")

	if __name__ == "__main__":
    	sys.exit(run())

b = Button(master, text="get", width=10, command=callback)
b.pack()

mainloop()
e = Entry(master, width=50)
e.pack()
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
