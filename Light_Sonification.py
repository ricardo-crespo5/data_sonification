# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:21:35 2024

@author: rcres
"""

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import wave




sample_rate = 30
total_time = 60 * 15
#skip = 60 * 60 * 2 * sample_rate

ONE_D = np.empty(total_time * sample_rate, dtype=object).astype(np.double)
fields = ['Time', 'Acc']
sums = 0

with open(f'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/{sample_rate}_downsampled_light.csv', 'w', newline='') as write:
    with open('C:/Users/rcres/Documents/Spyder/Sample_Rate/brightness.csv') as file:
        csv_reader = csv.reader(file, delimiter = ',')
        
        current = next(csv_reader)
        
        for i in range(total_time * sample_rate):
            ONE_D[i] = float(current[0])
            current = next(csv_reader)
              
        #csvwriter = csv.writer(write)
        #csvwriter.writerow(fields)
        #csvwriter.writerows(samples)

#Audio
audio_sr = 44100
audio = pd.Series(audio_sr * total_time * [np.nan])

#Sparse samples into audio array
iii = 0
for i in range(0, audio_sr * total_time, int(audio_sr/sample_rate)):
    audio[i] = ONE_D[iii]
    iii += 1

#Audio samplerate aproximation using interpolation
audio = pd.Series(audio)
audio = audio.interpolate(method="polynomial", order=3)
audio = audio.ffill()



audio = savgol_filter(audio, int(audio_sr/2)-1, 3)
#audio = audio.clip(1, 0)
#Normalization
audio = audio - np.min(audio)
audio = (audio - np.min(audio)) / (np.max(audio) - np.min(audio))
#plt.plot(audio)


#Sine wave modulation
freq = 250
rec = np.empty(audio.size)

for i in range(audio.size):
    rec[i] =  np.sin((audio[i] * freq) * 2 * np.pi * (i/audio_sr) + 100 * 2 * np.pi * (i/audio_sr))

#Audio normalization to 16 Bit-Depth
rec = np.int16(rec * 32767)

def array_to_wav(data, sample_rate, file_name, bit_depth=16):
    # Open a new WAV file
    with wave.open(file_name, 'wb') as wf:
        # Set parameters
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(bit_depth // 8)  # Sample width in bytes
        wf.setframerate(audio_sr)  # Sample rate
        wf.setcomptype('NONE', 'not compressed')  # Compression type

        # Write header
        wf.writeframes(b'')  

        # Write audio data
        wf.writeframes(data.tobytes())


# Write to WAV file
array_to_wav(rec, audio_sr, 'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/BNO_DATA/light.wav')
    