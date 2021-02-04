# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 12:03:39 2021

@author: jmami
"""


import speech_recognition as sr 
import moviepy.editor as mp
from gtts import gTTS
from io import BytesIO
import winsound
from playsound import playsound
import os
import streamlit as st

# import required libraries 
import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv 
import numpy as np
import sys
#import parselmouth
#from parselmouth.praat import call
#from parselmouth.praat import run_file
import matplotlib.pyplot as plt


# Sampling frequency 
freq = 16000

# Recording duration 
duration = 1
flag=True

def myplaysound(filename):
    # plays audio file filename in streamlit
    # have to click button though
    audio_file = open(filename,"rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/ogg")
    # audio_file.close
    # os.remove(filename)
    st.write('Click play button to play')

i=-1
while flag:
    i=i+1
    # Start recorder with the given values 
    # of duration and sample frequency
    recarr=np.transpose(np.array([[0],[0]]))
    sndarr=np.transpose(np.array([[0],[0]]))
    thold = 0.01
    
    flag=True  #no audio yet
    while np.max(recarr[:,0])<thold:
        for i in range(200): 
            # print(i)
            recording = sd.rec(int(duration * freq), 
        				samplerate=freq, channels=2) 
            sd.wait()
            recarr=np.concatenate((recarr,recording))
            # if np.max(recording[:,0])>thold:
                # sndarr=np.concatenate((sndarr,recording))
            # check for 1 s pause
            t1sec=int(freq)
            if (i>2 and np.max(recording[:,0])<thold):
                break
    
    # Record audio for the given number of seconds 
    sd.wait() 
    
    
    # Convert the NumPy array to audio file 
    # wv.write("recording1.wav", recarr, freq, sampwidth=2)
    wv.write("praat_out.wav", recarr, freq, sampwidth=2)
    # run_file('p_convert2.praat')
  
    r = sr.Recognizer()
    
    # audio=sr.AudioFile("glasses1.wav")
    # audio=sr.AudioFile("recording0.wav")
    audio=sr.AudioFile("praat_out.wav")
    
    
    with audio as source:
      audio_file = r.record(source)
    try:
        result_google = r.recognize_google(audio_file)
        # result_ibm = r.recognize_ibm(audio_file,"apikey",'LRe5UvZaK4W0nshNIxe2-3cTLEDncpjCnmrceSIormUT')
        # print(result_google,result_ibm)
        
        # exporting the result 
        with open('recognized.txt',mode ='w') as file: 
           file.write("Recognized Speech:") 
           file.write("\n") 
           # file.write(result_ibm['alternative'][0]['transcript']) 
           file.write(result_google['alternative'][0]['transcript']) 
           # print("ready!")
        
        mywords = result_google['alternative'][0]['transcript']
        if (mywords=='bye-bye' or mywords=='bye bye' or mywords=='Popeye') :
            # print('bye bye')
            mywords="bye-bye"
            st.write(mywords)
            tts=gTTS(mywords)
            fni='tempst'+str(i)+'.mp3'
            tts.save(fni)
            myplaysound(fni)
            flag=False
            sys.exit()
        print(mywords)
        st.write(mywords)
        tts=gTTS(mywords)
        fni='tempst'+str(i)+'.mp3'
        tts.save(fni)
        # winsound.PlaySound('day1.wav',winsound.SND_ASYNC)
        myplaysound(fni)
        recarr=np.transpose(np.array([[0],[0]]))
        # os.remove(fni)
    except:
        mywords="I did not understand. Please try again"
        st.write(mywords)
        tts=gTTS(mywords)
        fni='tempst'+str(i)+'.mp3'
        tts.save(fni)
        # winsound.PlaySound('day1.wav',winsound.SND_ASYNC)
        myplaysound(fni)
        recarr=np.transpose(np.array([[0],[0]]))
        # print('speech not recognized, try again...')
    
# delay=input('Press enter to finish')