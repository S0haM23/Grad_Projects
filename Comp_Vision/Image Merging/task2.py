# 1. Only add your code inside the function (including newly improted packages). 
#  You can design a new function and call the new function in the given functions. 
# 2. For bonus: Give your own picturs. If you have N pictures, name your pictures such as ["t3_1.png", "t3_2.png", ..., "t3_N.png"], and put them inside the folder "images".
# 3. Not following the project guidelines will result in a 10% reduction in grades

import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

def stitch(imgmark, N=4, savepath=''): #For bonus: change your input(N=*) here as default if the number of your input pictures is not 4.
    "The output image should be saved in the savepath."
    "The intermediate overlap relation should be returned as NxN a one-hot(only contains 0 or 1) array."
    "Do NOT modify the code provided."
    imgpath = [f'./images/{imgmark}_{n}.png' for n in range(1,N+1)]
    imgs = []
    for ipath in imgpath:
        img = cv2.imread(ipath)
        imgs.append(img)
    result = []
    for y in range (len(imgs)): 
        for x in range (y,len(imgs)):
            if x!=y : 
                if len(result) != 0 :
                    img1 = result
                else:
                    img1 = imgs[y] 
                img2 = imgs[x]
    
                orb = cv2.ORB_create(nfeatures=2000)
    
                # Find the key points and descriptors with ORB
                keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
                keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
    
                bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)
    
                # Find matching points
                matches = bf.knnMatch(descriptors1, descriptors2,k=2)
                
                ## matcher from scratch       
                # rows = descriptors2.shape[0]
                # for x in range(rows):
                #     matches = []
                #     for y in range(rows):

                #         sub = np.subtract(descriptors1[x],descriptors2[y])

                #         summ = np.sum(np.square(sub))

                #         elem = np.sqrt(summ)
                #         matches.append(elem)
                #     m = np.amin(matches)
                #     matches.remove(np.amin(matches))
                #     n = np.amin(matches)
                #     if m < 0.7*n:
                #         good.append(m) 
                       # query_idx.append(x)
                       # train_idx.append(y)

                
                
                
                # Finding the best matches
                good = []
                for m, n in matches:
                    if m.distance < 0.8 * n.distance:
                        good.append(m)
                def warpImages(img1, img2, H):
    
                    rows1 = img1.shape[0]
                    rows2 = img2.shape[0]
                    col1 = img1.shape[1]
                    col2 = img2.shape[1]
    
                    dist_1 = np.array([[0,0], [0, rows1],[col1, rows1], [col1, 0]],dtype='float32').reshape(-1, 1, 2)
                    # making a temporary image 2 array to transform its perpestive WRT image 1
                    temp_dist = np.array([[0,0], [0,rows2], [col2,rows2], [col2,0]],dtype='float32').reshape(-1,1,2)
    
                    # When we have established a homography we need to warp perspective
                    # Change field of view
                    dist_2 = cv2.perspectiveTransform(temp_dist, H)
    #                 print(dist_2)
                    dist = np.concatenate((dist_1,dist_2), axis=0)
    
                    [x_min, y_min] = np.int32(dist.min(axis=0).ravel() - 0.5)
                    [x_max, y_max] = np.int32(dist.max(axis=0).ravel() + 0.5)
    
                    translation_dist = [-x_min,-y_min]
    
                    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])
    
                    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
                    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:col1+translation_dist[0]] = img1
    
                    return output_img


                MIN_MATCH_COUNT = 10
    
                if len(good) > MIN_MATCH_COUNT:
    
                    # Establishing a homography matrix
                    M, _ = cv2.findHomography(np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2),np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2), cv2.RANSAC,5.0)
    
                    result = warpImages(img2, img1, M)
                    if result.shape > (1100,1100):
                        result = cv2.resize(result,(900,800))    

                    cv2.imshow('result',result)
                    
                    cv2.waitKey(0)
                    cv2.destroyAllWindows() 
                        
    overlap_arr = np.array(result)                          
    return overlap_arr
if __name__ == "__main__":
    #task2
    overlap_arr = stitch('t2', N=4, savepath='task2.png')
    with open('t2_overlap.txt', 'w') as outfile:
        json.dump(overlap_arr.tolist(), outfile)
    #bonus
    overlap_arr2 = stitch('t3', savepath='task3.png')
    with open('t3_overlap.txt', 'w') as outfile:
        json.dump(overlap_arr2.tolist(), outfile)


