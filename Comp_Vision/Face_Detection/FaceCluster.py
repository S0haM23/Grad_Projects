import face_recognition
import cv2
import glob
import json
import re
import os
import numpy as np
from PIL import Image
import sys 


path_arg = sys.argv[1]
K = int(path_arg.split("_")[-1])
if '~' in path_arg:
    path_arg = ''.join(sys.argv[1].split("~"))
path = path_arg + "/*"


filenames = glob.glob(path)
filenames.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

images = [cv2.imread(img) for img in filenames]

face_cascade = cv2.CascadeClassifier('Model_Files/haarcascade_frontalface_default.xml')
e_list = []
faces = []
crop = []
print("Total images found : ", len(images))
print("Number of Unique Faces Identified : ", K)
List_1 = [*range(1,K+1, 1)]
for i in range (len(images)): 
# Load the jpg file into a numpy array
    img = images[i]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.2,4)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(128,128,128),2)
        roi = img[y:y+h, x:x+w]
        crop.append(roi)
        location = (x,y,w,h)
#         print(location)
        boxes = [(y,x+w,y+h,x)]

        enc = face_recognition.face_encodings(img,boxes)
        e_list.append(enc)
## Creating random clusters
import random
rand_list = []

for i in range(0,K):
    n = random.randint(1,len(images))
    rand_list = random.sample(range(1, len(images)), K)
#     if n not in rand_list: rand_list.append(n) # avoid repetition 

clusters = []
for i in rand_list:
    clusters.append(e_list[i])
# print(clusters)
for x in range(30):
    
    dist = np.zeros((len(e_list), len(clusters))) ## row,col
    ## Eucladian dist between clusters and others
    point1 = np.array(clusters)
    point2 = np.array(e_list)
#     print(np.mean(clusters))
    for i in range(len(clusters)):
        for j in range(len(e_list)):
            distance = np.linalg.norm(point1[i] - point2[j])
            dist[j,i] = distance     
    # print(dist)
    minim = np.argmin(dist,axis=1)+1 ## gets the index of the minimum value in the cluster

#     count = 0
#     for i in List_1:

#         if minim.tolist().count(i) != 0:
#             count+=1
# #         print(count)
#     if count == K:
#     print(minim) ## shows which image index corresponds to which cluster
    
    arr1 = []
    for p in range(1,max(minim)+1):
        arr1.append(np.where(minim==p)[0])
#     print(arr1)
    clusters.clear()
    avg = []
    for i in arr1:
        avrg = []

        for j in i:
            avrg.append(e_list[j])
        avg = np.mean(avrg, axis = 0)   
#         print(avg,'\n\n')/
        clusters.append(avg)
#     else:
#         continue


## face cluster mosiac

arr2 = [] ## SAVES ALL IMAGES IN THIS ARRAY
cluster_of_faces = []
for p in range(1,max(minim)+1):
        arr2.append(np.where(minim==p)[0])
# print(arr2[0])   
imgs_list = []
im_lst = []
for i in range(len(arr2)):
    
    for j in arr2[i]:
#         print(j)
        reshape = cv2.resize(crop[j],(97,97))             
        imgs_list.append(reshape)
    v_img = cv2.hconcat(imgs_list)
## Uncomment if want to visualize clusters
#     cv2.imshow('CLUSTER_'+str(i+1), v_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    imgs_list.clear() 


## cluster.json
clust_list = []
for i in range(len(arr2)):
    list_tail = []
    for j in arr2[i]:
        head, tail = os.path.split(filenames[j])
        list_tail.append(tail)
        suf_res = ['img' + sub  for sub in list_tail]
    element = {"cluster_no": i ,"elements": suf_res} 
    clust_list.append(element)    

#the result json file name
output_json = "clusters.json"
#dump json_list to result.json
with open(output_json, 'w') as f:
    json.dump(clust_list, f)  
    
print("success")