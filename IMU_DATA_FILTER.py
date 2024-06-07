# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:21:35 2024

@author: rcres
"""

import numpy as np
import csv

sample_rate = 10
total_time = 4 * 60 * 60

samples = np.empty(total_time * sample_rate, dtype=object)
#skipinitialspace=True
fields = ['Time','Acc','','', 'Magn','','', 'Gyro','','', 'Euler','','', 'Quat','','','', 'lin_acc','','', 'Grav','','']

with open(f'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/{sample_rate}_downsampled.csv', 'w', newline='') as write:
    with open('C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/BNO_DATA/EMU_BNO055.csv') as file:
        csv_reader = csv.reader(file, delimiter = ',')
        
        current = next(csv_reader)
        current = next(csv_reader)
        new = current
        
        for i in range(total_time):
            rows = []
            index = 1
            i2 = 0
            amount = 0
            
            while current[0] == new[0]:
                amount += 1
                rows.append(new)
                new = next(csv_reader)
            
            frac = 0
            for i1 in range(i * sample_rate,(sample_rate * i) + sample_rate):
                samples[i1] = rows[round(frac)]
                frac += ((amount-1)/sample_rate)
            current = new
              
        csvwriter = csv.writer(write)
        csvwriter.writerow(fields)
        csvwriter.writerows(samples)