# import pyaudio
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# exit()

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
                    input=True,
                    input_device_index=2,
                    frames_per_buffer=CHUNK)
    
    print("Recording")
    while True:
        q.put(stream.read(CHUNK, exception_on_overflow=False))
        
        
if __name__ == '__main__':
    queue = mp.Queue()
    p = mp.Process(target=feed_queue, args=(queue,))
    p.start()


    import pygame.mixer
    pygame.mixer.pre_init(48000, -16, 1,512, allowedchanges=0)
    pygame.mixer.init()
    pygame.init()
    S = pygame.mixer.Sound
    while True:
        d = queue.get()
        S(d).play()