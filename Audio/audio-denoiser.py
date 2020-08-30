import multiprocessing as mp
import time
import sys

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
    count1=0;
    while True:
        q.put(stream.read(CHUNK, exception_on_overflow=False))
        

def pop_queue(q):
    import pygame.mixer

    pygame.mixer.pre_init(48000, -16, 1,512,devicename='Line 1 (Virtual Audio Cable)', allowedchanges=0)
    pygame.mixer.init()
    pygame.init()

    pygame.mixer.set_num_channels(2)
    channel = pygame.mixer.Channel(0)
    while True:
        d = queue.get()
        S = pygame.mixer.Sound(buffer=d)
        channel.queue(S)


if __name__ == '__main__':
    queue = mp.Queue()
    p = mp.Process(target=feed_queue, args=(queue,))
    p.start()
    pop_queue(queue)


