## PART A OF PROJECT
import cv2
import glob
import json
import numpy as np
import re
import os
import argparse
import sys


path_arg = sys.argv[1]
if '~' in path_arg:
    path_arg = ''.join(sys.argv[1].split("~"))
path =  path_arg + "/images/*"
filenames = glob.glob(path)
filenames.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
# print(sys.argv)
print("Number of images found:", len(filenames))
images = [cv2.imread(img) for img in filenames]
face_cascade = cv2.CascadeClassifier('Model_Files/haarcascade_frontalface_default.xml')
json_list = []
for k in range (len(images)): 
# Load the jpg file into a numpy array
    img = images[k]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.2,4)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(128,128,128),2)
        roi = img[y:y+h, x:x+w]
#         location = (x,y,w,h)
#         print(location)
        head, tail = os.path.split(filenames[k])
        element = {"iname": tail, "bbox": [float(x),float(y),float(w),float(h)]} 
        json_list.append(element)    
print("Number of faces found:", len(json_list))    
#the result json file name
output_json = "results.json"
#dump json_list to result.json
with open(output_json, 'w') as f:
    json.dump(json_list, f)    
    
print("DONE")