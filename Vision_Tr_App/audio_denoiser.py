from SpeechDenoiser import SpeechDenoiser
import multiprocessing as mp
import time
import sys
import os
import numpy 

CHANNELS = 1
CHUNK = 1024
RATE = 48000

def feed_queue(q):
    import pyaudio
    import numpy

    FORMAT = pyaudio.paInt16
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=1,
                    frames_per_buffer=CHUNK)
    
    print("*Recording*")
    while True:
        q.put(stream.read(CHUNK, exception_on_overflow=False))
        
def pop_queue(q):
    import pygame.mixer

    pygame.mixer.pre_init(16000, -16, 1,512,devicename='Line 1 (Virtual Audio Cable)', allowedchanges=0)
    pygame.mixer.init()
    pygame.init()

    pygame.mixer.set_num_channels(1)
    channel = pygame.mixer.Channel(0)
    while True:
        d = q.get()
        S = pygame.mixer.Sound(buffer=d)
        channel.queue(S)

def filter_queue(hearing,filtering):
    import numpy as np
    from io import BytesIO
    import wave
    import pygame.mixer

    denoiser=SpeechDenoiser();
    while True:
        frames48k=[]
        for i in range(70):
            if hearing.empty():
                time.sleep(0.15) 
            else:
                frames48k.append(hearing.get())
            
        frames16k=denoiser.resample_ratecv(b''.join(frames48k),48000,16000)
        samples16k=denoiser.get_all_samples(frames16k[0])
        samples16k=bytearray(samples16k)

        waveFile = wave.open("tmp.wav", 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(16000)
        waveFile.writeframes(samples16k)
        waveFile.close() 

        time.sleep(0.1);
        
        noisyAudio, sr=denoiser.read_audio("tmp.wav", sample_rate=16000)
        filtered_np = denoiser.reduceNoiseMain(noisyAudio);
        
        pygame.mixer.pre_init(16000, -16, 1,512,devicename='Transcript (VB-Audio Virtual Cable)', allowedchanges=0)
        pygame.mixer.init()
        pygame.init()
        
        time.sleep(0.1);
        
        sounda= pygame.mixer.Sound("tmp_f.wav")
        sounda.play()

def main_audio_denoiser():
    queueHeard = mp.Queue()
    queueFiltered = mp.Queue()
    hearing = mp.Process(target=feed_queue, args=(queueHeard,))
    filtering = mp.Process(target=filter_queue, args=(queueHeard,queueFiltered))
    hearing.start()
    time.sleep(1);
    filtering.start();
    #pop_queue(queueFiltered)

