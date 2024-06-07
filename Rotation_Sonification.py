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




sample_rate = 10
total_time = 5 * 60
#skip = 60 * 60 * 2 * sample_rate

samples = np.empty(total_time * sample_rate, dtype=object)
ONE_D = np.empty(total_time * sample_rate, dtype=object).astype(np.double)
fields = ['Time', 'Acc']
sums = 0

with open(f'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/{sample_rate}_downsampled.csv', 'w', newline='') as write:
    with open('C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/BNO_DATA/EMU_BNO055.csv') as file:
        csv_reader = csv.reader(file, delimiter = ',')
        
        current = next(csv_reader)
        current = next(csv_reader)
        new = current
        #p = False
        
        for i in range(total_time):
            rows = []
            index = 1
            i2 = 0
            amount = 0
            
            while current[0] == new[0]:
                amount += 1
                rows.append(new)
                new = next(csv_reader)
                
                """
                #skip
                if(p == False):
                    for s in range(skip):
                        new = next(csv_reader)
                    p = True
                """
                
            
            frac = 0
            for i1 in range(i * sample_rate,(sample_rate * i) + sample_rate):
                convert = [rows[round(frac)][1].replace('(', '').strip(), rows[round(frac)][2], rows[round(frac)][3].replace(')', '').strip()]
                
                if(convert[0] != 'None'):
                    convert = [float(convert[0]), float(convert[1]), float(convert[2])]
                else:
                    convert = [np.nan, np.nan, np.nan]

                samples[i1] = convert
                ONE_D[i1] = convert[0]
                frac += ((amount-1)/sample_rate)
            current = new
              
        #csvwriter = csv.writer(write)
        #csvwriter.writerow(fields)
        #csvwriter.writerows(samples)

#Interpolation
ONE_D = pd.Series(ONE_D)
ONE_D = ONE_D.interpolate(method="polynomial", order=2)

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
audio = audio.interpolate(method="polynomial", order=2)
audio = audio.ffill()

#Normalization and smoothing of data
data = audio.clip(-1, 1)
data = savgol_filter(data, 15, 3)

#Sine wave modulation
freq = 300
rec = np.empty(data.size)

for i in range(data.size):
    rec[i] =  np.sin((freq * 2 * np.pi * (i/audio_sr)) + ((freq/2) * (data[i])))

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
array_to_wav(rec, audio_sr, 'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/BNO_DATA/output.wav')
    