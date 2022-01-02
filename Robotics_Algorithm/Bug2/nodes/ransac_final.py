#! /usr/bin/env python
from visualization_msgs.msg import Marker
import rospy
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
import numpy as np
import math
import random
# import matplotlib.pyplot as plt
thresh = 0.1 # -- distance threshold
dist = []
Px,Py = [],[]
n = 1

def ransac(laser):
    global pts,n,display,marker1,dist,thresh,Px,Py
    # print("getting in ransac")
    increm = laser.angle_increment
    minang = laser.angle_min
    ranges = laser.ranges
    pts = []
    i = 0
    for r in ranges:
        i +=1
        if r<3:
            t = minang+i*increm
            x = r*math.cos(t)
            y = math.sin(t)
            pts.append((x,y))
    pts.sort()
    # print("points",len(pts))

    marker1 = Marker()
    # print("running")
    x_cord,y_cord = [],[]
    pub = rospy.Publisher("ransac", Marker, queue_size=10)
    for k in range(0,50):
        start_x,start_y,end_x,end_y = 0,0,0,0
        # print("in 1st loop")
        dist = []
        if len(pts) != 0:
            # print("get into if loop")
            idx = 0
            idx_2 = len(pts)-1        
            if idx != idx_2 :
                # print("in 2nd if loop")
                x_val = pts[idx][0],pts[idx_2][0]
                y_val = pts[idx][1],pts[idx_2][1]    ## get model of line
                slope = np.diff(y_val)/np.diff(x_val)
                inter = pts[idx][1] - slope*pts[idx][0]
                for P in pts:
                    d = abs ((slope*P[0] - P[1] + inter)) / math.sqrt((slope*slope) + 1)
                    # print("printing Distance", d)
                    if d <= thresh:  
                        dist.append(P)
                        # n+=1
                    # if len(dist)/len(pts) >= 0.35:          
                    start_x = pts[idx][0]
                    start_y = pts[idx][1]
                    end_x = pts[idx_2][0]
                    end_y = pts[idx_2][1]

                    # for w in dist:
                    #     pts.remove(w)

    marker1.header.frame_id = "base_link"
    marker1.header.stamp =rospy.Time.now()
    marker1.ns = "ransac"
    marker1.id = 0
    marker1.type = Marker.LINE_STRIP # Marker.LINE_STRIP #Marker.POINTS # The LINE_LIST type creates unconnected lines out of each pair of points, i.e. point 0 to 1, 2 to 3, etc.
    marker1.action = Marker.ADD

    x_cord.append(start_x)
    y_cord.append(start_y)
    x_cord.append(end_x)
    y_cord.append(end_y)

    for i in range(0,2):
        p = Point()
        p.x = x_cord[i]
        p.y = y_cord[i]
        marker1.points.append(p)

    marker1.scale.x = 0.05
    marker1.scale.y = 0.0
    marker1.scale.z = 0.0

    marker1.pose.orientation.x = 0.0
    marker1.pose.orientation.y = 0.0
    marker1.pose.orientation.z = 0.0
    marker1.pose.orientation.w = 1.0

    marker1.color.r = 1.0
    marker1.color.g = 0.0
    marker1.color.b = 0.5
    marker1.color.a = 1.0
    marker1.lifetime = rospy.Duration()
    print(x_cord,y_cord)
    pub.publish(marker1)

if __name__ == '__main__':
    rospy.init_node("ransac")
    rospy.Subscriber("/base_scan", LaserScan, ransac)
    rospy.spin()

