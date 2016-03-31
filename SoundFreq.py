# Python Art - Sound Frequencies
#
# This code generates Python Turtle images after analysing 5 seconds of recorded audio or a pre-recorded 16 bit WAV file
#
# The project has been inspired and helped through lots of examples and questions on forums or websites including:
#   http://stackoverflow.com/questions/1797631/recognising-tone-of-the-audio
#   http://stackoverflow.com/questions/9634478/unable-to-install-pyaudio-on-osx-lion/10290595#10290595
#   https://gist.github.com/mabdrabo/8678538
#   http://stackoverflow.com/questions/2648151/python-frequency-detection
#   https://gist.github.com/livibetter/4118062
#
# Thanks to these programmers!
#
# CC0 Ian Simpson, 31st March 2016 @familysimpson

import pyaudio
import wave
import numpy as np
import turtle
import random

chunk = 2048
RECORD_SECONDS = 5
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "file.wav"
freq = []

# Circleshade is where the individual shapes are drawn for each frequency from the audio analysis. Hoping to add some
# fading colours in future revisions but hitting issues with colorsys.rgb_to_hls and vice versa at the moment

def circleshade(x,y,size,color,iteration):
    t1.penup()
    t1.pensize(7-iteration)
    lstRGB = color # temporary assignment, see header for details
    t1.color(lstRGB[0],lstRGB[1],lstRGB[2])
    t1.goto(x, y-(size/2)-iteration) # try to centre the new circles around the old ones
    t1.pendown()
    t1.circle(size)
    # recurse 6 times, increasing size of circle each time (this is where fading colours will make impact)
    if iteration < 6:
        circleshade(x,y,size+(iteration*iteration),lstRGB,iteration+1)

# recordSound is where 5 seconds of audio is recorded for use by the procedure loadSound later.

def recordSound():
    # Read in a WAV and find the freq's

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=chunk)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        frames.append(data)
    print("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

# loadSound uses the wave library to read in a WAV file and then analyse it using FFT to generate a list of audio frequencies for visualisation.

def loadSound(filename):

    # open up a wave
    wf = wave.open(filename, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = RATE,
                    output = True)

    #ANALYSE AUDIO FILE AND BUILD LIST

    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):

        # read some data
        data = wf.readframes(int(chunk/2))
        # play stream and find the frequency of each chunk
        #print("len(data) = ",str(len(data))," & chunks*width = ",str(chunk*swidth))
        while len(data) == chunk*swidth:
            # write data out to the audio stream
            stream.write(data)
            # unpack the data and times by the hamming window
            indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                                 data))*window
            # Take the fft and square each value
            fftData=abs(np.fft.rfft(indata))**2
            # find the maximum
            which = fftData[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fftData)-1:
                y0,y1,y2 = np.log(fftData[which-1:which+2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                # find the frequency and output it
                freq.append ((which+x1)*RATE/chunk)
            else:
                freq.append(which*RATE/chunk)
            #read some more data
            data = wf.readframes(int(chunk/2))

    stream.close()
    p.terminate()

# Main program
# Displays an option to record sound or load a pre-recorded sound. Sets variable theFilename accordingly so that correct file is loaded. Then turtle screen is set up to create visualisation.

option = input("[1] Record sound, [2] Load sound")
if option == "1":
    recordSound()
    theFilename = WAVE_OUTPUT_FILENAME
else:
    theFilename = input("Enter the filename")
loadSound(theFilename)

#VISUALISE FREQUENCIES

wn = turtle.Screen()
w = 600
wscale = w/(max(freq)-min(freq))

h = 600
yarea = h / len(freq)

wn.screensize(w,h)
bgcolor = (random.randrange(0,255)/255.,random.randrange(0,255)/255.,random.randrange(0,255)/255.)
wn.bgcolor(bgcolor) # set background colour of turtle screen.

t1 = turtle.Turtle()
turtle.colormode(1.0)

wn.tracer(False) # setting tracer to False makes the image draw much faster
count = 0
for xpos in freq: #loop for each frequency in the freq list
    thiscolor = (random.randrange(0,255)/255.,random.randrange(0,255)/255.,random.randrange(0,255)/255.)
    circleshade((xpos*wscale)-(w/2),(yarea*count)-(h/2),random.randrange(int(yarea/2),int(yarea*3)),thiscolor,0)
    count += 1
wn.tracer(True) # setting tracer back to True at the end means that the image is shown to the user
wn.exitonclick() # show Turtle screen until user clicks to exit