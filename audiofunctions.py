######################## Notes   ##################################
'''
- scipy.io.wavfile.read is picky with types
    - Cannot read wav files with 24-bit data: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
    - Supports:
        - 32-bit floating point [Getting Format Error]
        - 32-bit PCM
        - 16-bit PCM
        - 8-bit PCM

- Parallel playback of multiple files will have to be handled by threads
'''
######################## Imports ##################################

# Native Python library
import sys

# Signal Processing Libraries
import wave
import numpy
import scipy.io.wavfile, scipy.io
import scipy.signal

# GUI Library
import Tkinter
from tkFileDialog import *

# Sound Libraries
#import soundfile as sf
import pyaudio
import pygame
import sounddevice as sd
import time

########################## Main ###################################

# Ask user to select the track and store the file's path
# filePath = askopenfilename(initialdir = "./", title = "Select Track", filetypes = (("WAV files","*.WAV"),("All files","*.*")))


def create3DAudio(filePath, listOfSounds, azimuth, elevation):
    # Open file at given path
    fileToRead = wave.open(filePath, "r")
    #print("Azimuth, ", azimuth)
    #print("Elevation, ", elevation)
    #placeholders:
    azimuth = 5
    elevation = 4

    # Read opened .WAV file and store the sample rate (usually 44100 Hz or 44.1 kHz) and the audio data
    sampleRate, readData = scipy.io.wavfile.read(filePath)

    # Take in command line arguments for the azimuth, elevation, and radius
    #programName = sys.argv[0]
    #arguments = sys.argv[1:]
    #azimuth = int(arguments[0])
    #elevation = int(arguments[1])
    radius = 5

    # Ask user to select HRTF
    #HRTFToUse = askopenfilename(initialdir = "../CIPIC_hrtf_database/standard_hrir_database/subject_127", title = "Select HRTF")
    HRTFToUse = "../../Desktop/CIPIC_hrtf_database/standard_hrir_database/subject_127/hrir_final.mat"
    # Load hrtf
    hrtf = scipy.io.loadmat(HRTFToUse)

    # Accessing Head-Related Impulse Responses (HRIR) for the left and right ears & Interaural Time Difference (ITD)
    hrir_l =  hrtf['hrir_l']
    hrir_r = hrtf['hrir_r']
    ITD = hrtf['ITD']

    # List of Azimuths (25 locations, as per the CIPIC database)
    negAzimuths = [-80, -65, -55, -45]
    intervalsOf5 = numpy.arange(-40,45,5).tolist()
    posAzimuths = [45 , 55 , 65, 80]
    azimuths = negAzimuths + intervalsOf5 + posAzimuths

    # List of Elevations (50 locations, as per the CIPIC database)
    rangeFrom0to49 = numpy.arange(0.0,50.0,1.0)
    elevations = -45 + 5.625*rangeFrom0to49
    elevations = elevations.tolist()

    #print azimuths
    #print elevations

    # Initializing lists for .WAV input
    wav_left = []
    wav_right = []
    soundToPlay = []

    # Getting all of the HRIRs for the left and right ears using the given azimuth and elevation
    lft = numpy.squeeze(hrir_l[azimuth, elevation, :])
    rgt = numpy.squeeze(hrir_r[azimuth, elevation, :])

    # Creating a delay using the ITD (in ms)
    delay = ITD[azimuth, elevation]
    delaySampleRate = numpy.floor(delay* (sampleRate/1000))

    # Transposing arrays for concatenation
    lftTransposed = numpy.transpose(lft).tolist()
    rgtTransposed = numpy.transpose(rgt).tolist()

    # Creating array of zeros proportional to the ITD
    zerosDelayArr = numpy.zeros(numpy.arange(1,numpy.absolute(delaySampleRate),1).shape).ravel().tolist()

    # Getting the left channel of the stereo audio data
    readDatalft = readData#numpy.delete(readData, 0, axis=0).ravel()

    # Getting the right channel of the stereo audio data
    readDatargt = readData#numpy.delete(readData, 0, axis=0).ravel()

    ################################################################
    #readDatalftTransposed = numpy.transpose(readDatalft).tolist()
    #readDatargtTransposed = numpy.transpose(readDatargt).tolist()
    ################################################################

    # Convolving the left HRIRs with the left channel of the audio data
    convolvedlft = numpy.convolve(lft, readDatalft).tolist()

    # Convolving the right HRIRs with the right channel of the audio data
    convolvedrgt = numpy.convolve(rgt, readDatargt).tolist()

    ################################################################
    # Creating array of zeros to pad the convolved audio
    #zerosArr = numpy.zeros((1, int(delay))).ravel().tolist()
    ################################################################

    ## If the sound is on the left side, pad the right side
    #if azimuth < 13:
    #    lft = lftTransposed + zerosDelayArr
    #    rgt = zerosDelayArr + rgtTransposed
    #
    ## Else if the sound is on the right side then pad the left side
    #else:
    #    lft = zerosDelayArr + lftTransposed
    #    rgt = rgtTransposed + zerosDelayArr


    # Padding the left and right convolved audio channels
    if azimuth < 13:
        wav_left =  convolvedlft + zerosDelayArr
        wav_right = zerosDelayArr + convolvedrgt
    else:
        wav_left =  zerosDelayArr + convolvedlft
        wav_right = convolvedrgt + zerosDelayArr

    # Creating two channel stereo audio array for playback
    soundToPlay = [wav_left, wav_right]
    #soundToPlay = numpy.asarray(soundToPlay)
    #soundToPlay = numpy.transpose(soundToPlay)

    #listOfSounds = numpy.concatenate(listOfSounds, soundToPlay)
    #listOfSounds.append(soundToPlay)
    listOfSounds.append(soundToPlay)
    #print(listOfSounds)
    #print(len(listOfSounds))

    #scipy.io.wavfile.write("soundToPlay-mono.wav", sampleRate, soundToPlay)

def addSounds(soundToPlay, listOfSounds):
    # print(len(soundToPlay))
    for sound in listOfSounds:
        if sound is not None:
            soundToPlay = soundToPlay + sound
            # print(numpy.shape(sound))
    return soundToPlay

def playSound(soundToPlay, sampleRate):
    soundToPlay = numpy.asarray(soundToPlay)
    soundToPlay = numpy.transpose(soundToPlay).ravel()

    # Normalizing audio to range between [-1,1]
    min = soundToPlay.min()
    max = soundToPlay.max()
    normalized = (((soundToPlay-min)/(max-min)) * 2) - 1

    # Playback the spatialized audio
    scipy.io.wavfile.write("soundToPlay-mono.wav", sampleRate, normalized)

    sd.play(normalized, sampleRate)
    time.sleep(5)
