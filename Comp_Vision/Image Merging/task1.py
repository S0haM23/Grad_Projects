#Only add your code inside the function (including newly improted packages)
# You can design a new function and call the new function in the given functions. 
# Not following the project guidelines will result in a 10% reduction in grades

import cv2
import numpy as np
import matplotlib.pyplot as plt

def stitch_background(img1, img2, savepath=''):
    "The output image should be saved in the savepath."
    "Do NOT modify the code provided."

    # Create our ORB detector and detect keypoints and descriptors
    orb = cv2.ORB_create(nfeatures=2000)
    # Find the key points and descriptors with ORB
    keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
    good = []
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)
    print('descriptors',descriptors1.shape)
    
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

    

    for m, n in matches:
        if m.distance < 0.9 * n.distance:
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
    
        dist = np.concatenate((dist_1,dist_2), axis=0)
    
        [x_min, y_min] = np.int32(dist.min(axis=0).ravel())
        [x_max, y_max] = np.int32(dist.max(axis=0).ravel())
    
        translation_dist = [-x_min,-y_min]
    
        H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])
    
        output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
        output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:col1+translation_dist[0]] = img1
    
        return output_img
    
    
    MIN_MATCH_COUNT = 10
    
    if len(good) > MIN_MATCH_COUNT:
        # Convert keypoints to an argument for findHomography
        pts_1 = np.array([ keypoints1[m.queryIdx].pt for m in good],dtype = 'float32').reshape(-1,1,2)
        pts_2 = np.array([ keypoints2[m.trainIdx].pt for m in good],dtype = 'float32').reshape(-1,1,2)
        
        # Establish a homography
        H, _ = cv2.findHomography(pts_1,pts_2, cv2.RANSAC,5.0)
    
        stitched = warpImages(img2, img1, H)
    
    ## foreground removal
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    boxes, weights = hog.detectMultiScale(stitched,
                                          winStride=(4, 4),
                                          padding=(4,4),
                                          scale=1.1)
    rectangle = stitched.copy()
    
    for (x, y, w, h) in boxes:
    
        cv2.rectangle(rectangle, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print('coord',x,y,x+w,y+h)
        for row in range (y,y+h):
            for col in range (x,x+w):
                if sum((stitched[row,col])) < 150:
                    stitched[row,col] = img2[(row),(col)]
    cv2.imshow('op',stitched)
    plt.show()
    cv2.imwrite(savepath,stitched)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return
if __name__ == "__main__":
    img1 = cv2.imread('./images/t1_2.png')
    img2 = cv2.imread('./images/t1_1.png')
    savepath = 'task1.png'
    stitch_background(img1, img2, savepath=savepath)


