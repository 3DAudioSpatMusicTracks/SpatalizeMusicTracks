import os
import sys
import time
import Tkinter, tkFileDialog
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
import numpy as np
import scipy.io.wavfile, scipy.io

#drumsFile = "Drums - Four Lights.wav"
#rhythmGuitarFile = "Rhythm Guitar - Four Lights.wav"

# bass = wave.open(bassFile, 'r')
bassFile = "hey.wav"
bassRate, bassData = scipy.io.wavfile.read(bassFile)

# Selecting HRTF for User (Double-Check)
HRTFToUse = tkFileDialog.askopenfilename()  # Opens Tkinter GUI and File Explorer for selecting .mat file
hrtf = scipy.io.loadmat(HRTFToUse)          # Opens file at stored path
# open(strip(HRTFToUse))

print hrtf



