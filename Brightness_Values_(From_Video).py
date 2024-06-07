# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:33:47 2024

@author: rcres
"""

import cv2
import csv
#import numpy as np

input_file = "C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/VEML_DATA/launch_4.mp4"
output_file = 'C:/Users/rcres/Documents/Spyder/Sample_Rate/Data/my_video.mp4'

def calculate_brightness(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Calculate the average pixel value
    brightness = cv2.mean(gray_frame)[0]
    return brightness

cap = cv2.VideoCapture(input_file)
brightness = []
print(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
i = 0

with open('C:/Users/rcres/Documents/Spyder/Sample_Rate/brightness.csv', 'w', newline='') as write:
    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()
    
        if not ret:
            break
    
        # Calculate brightness of the frame
        brightness.append([calculate_brightness(frame)])
        i += 1
        

        
    csvwriter = csv.writer(write)
    # Write the brightness value
    csvwriter.writerows(brightness)

# Release the video capture object
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()