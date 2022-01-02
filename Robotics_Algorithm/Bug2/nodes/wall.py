#! /usr/bin/env python

import rospy
import numpy as np
import matplotlib.pyplot as plt
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from tf import transformations
from time import sleep


state = 0               ## keeps a tab of wall follow state
counter = 0             ## just a counter   
theta = 0               ## eucladian angle
yaw = 0                 ## robot angle
x_init,y_init = 0,0     ## robo position @ t=0
lst = []
goal_x,goal_y = 4.5,9   ## get final destination   
intersect,current_pos = 0,0
d = 0.8
wall_follow_start = False
front = 0
def detection_callback(Laser): 
    global right,front,left,front_left,front_right,twist,ranges,increm,minang,inten,start,end,tip

    ranges = Laser.ranges
    inten = Laser.intensities
    minang = Laser.angle_min
    increm = Laser.angle_increment
    
    right=min(Laser.ranges[0:60])
    front_right=min(Laser.ranges[61:170])
    front= min(Laser.ranges[171:190])
    front_left= min(Laser.ranges[191:300])
    left= min(Laser.ranges[301:360])
    start = Laser.ranges[0]
    tip = Laser.ranges[180]
    end = Laser.ranges[360]

    twist = Twist()

def position_callback(odom):
    global counter,theta,yaw,x_init,y_init,twist
    global intersect,current_pos,lst
    global right,front,left,front_left,front_right,twist,ranges,increm,minang,inten,start,end,tip
    global wall_follow_start,goal_y,goal_x,xval,yval,err
    
    if counter== 0:
        x_init,y_init = odom.pose.pose.position.x,odom.pose.pose.position.y   ## get initial position of robot
        counter+=1
                                                                           
    slope = (goal_y - y_init) / (goal_x - x_init)                             ## slope of Line 
    intersect = goal_y - slope * goal_x                                       ## intercet of line --  these 2 would give EOL
    err = 0.06*intersect
    tol_1 = intersect-err                                                     ## set tolerance for error
    tol_2 = intersect+err
    xval = odom.pose.pose.position.x                                          ## get current robot positions
    yval = odom.pose.pose.position.y
    current_pos =  yval-(slope*xval)   ## get current position of robot wrt Line
                                             
    # print(wall_follow_start)
    # lst = np.linspace(round(tol_1,2),round(tol_2,2),150)
    # print(round(intersect,3),round(current_pos,3))
    quaternion = (
        odom.pose.pose.orientation.x,
        odom.pose.pose.orientation.y,                                         ## convert all angles to euler
        odom.pose.pose.orientation.z,
        odom.pose.pose.orientation.w)

    euler = transformations.euler_from_quaternion(quaternion)               
    yaw = math.degrees(euler[2])                                                ## get current orientation of robot WRT world
    theta = math.degrees(math.atan((goal_y-y_init) / (goal_x-x_init)))          ## get relative angle of line from robot
  
    if current_pos >= tol_1 and current_pos < tol_2 and front > d and not wall_follow_start :  # wall follow is false                ## if robot on euc. line 
            goal_seek()
    else:
        if current_pos >= tol_1 and current_pos < tol_2 :                ## if on line wall sollow start true
            wall_follow_start = True
        else:
            wall_follow_start = False
        wall_follow()                                              ## if robot not on goal line
        
def goal_seek():
    global right,front,left,front_left,front_right,twist,ranges,start,end,tip,state,current_pos,intersect,err
    state = 0
    global goal_x,goal_y,err,xval,yval
    # print("goal seek mode ON")
    if (round(xval,1),round(yval)) == (goal_x,goal_y):
        print("Reached Destination")
        twist.linear.x = 0
        twist.angular.z = 0
        pub.publish(twist)

    elif (round(xval,1),round(yval,1)) != (goal_x,goal_y):   ## robot coordinates != goal
        if round(yaw) != round(theta): 
            if xval == x_init:               
                twist.linear.x = 0                                      
                twist.angular.z = 0.2
                pub.publish(twist)
            else:
                twist.linear.x = 0                                      
                twist.angular.z = -0.2
                pub.publish(twist)
        if round(yaw) == round(abs(theta)):   
            twist.angular.z = 0
            twist.linear.x = 2
            pub.publish(twist)  
                    
        if round(intersect-current_pos,3) >= (err-0.05):
            twist.angular.z = 0.03
            twist.linear.x = 0.3
            pub.publish(twist)
   
def wall_follow():
    global right,front,left,front_left,front_right,twist,ranges,start,end,tip,state
    global goal_x,goal_y

    if  max(ranges) < 1 :# robot stuck in a corner
        twist.linear.x = 0
        twist.angular.z = -0.7
        pub.publish(twist)
    
    if  front < d and state != 1:  # detect obstaclt on left : hard turn right
        twist.linear.x = 0
        twist.angular.z = -0.5        
        pub.publish(twist)
        if front == 3: # if robot gets parallel to a wall stop spinning 
            twist.angular.z = 0  
            twist.linear.x = 2            
            state = 1             ## wall on left
            pub.publish(twist)
    
    elif  front > d and left > d:# and state == 1:# wall on robot's left -- nudge robot counter clock-wise
        twist.linear.x = 0
        twist.angular.z = 0.5
        pub.publish(twist)
    else:
        twist.linear.x = 2
        pub.publish(twist)

    if (round(xval,1),round(yval)) == (goal_x,goal_y):
        print("Reached Destination",(goal_x,goal_y))
        twist.linear.x = 0
        pub.publish(twist)

if __name__ == '__main__':
    global pub

    rospy.init_node("bug2")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/base_scan", LaserScan, detection_callback)
    sleep(0.6)
    rospy.Subscriber("/base_pose_ground_truth", Odometry,position_callback)

    rospy.spin()
