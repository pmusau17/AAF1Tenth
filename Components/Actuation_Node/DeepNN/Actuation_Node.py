#!/usr/bin/env python2.7
import sys
import os
import numpy as np
import math
import cv2
import rospy
#import IO
from deepnncar_components.msg import drive_param
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()

class Actuation:
    #define the constructor
    def __init__(self,racecar_name):
        self.cv_bridge=CvBridge()
        self.image_topic= '/' + str(racecar_name) +'/drive_parameters'

    def callback(self,data):
        print(data)
    	speed_pwm = data.velocity
    	steer_pwm = data.angle
        #IO.changeDutyCycle((speed_pwm, steer_pwm))
        #print("speed:%s steer:%s"%(speed_pwm,steering_pwm))

# def Actuation():
#     try:
#         rospy.init_node('Actuation_Node', anonymous=True)
#         rospy.Subscriber('drive_parameters', drive_param, callback)
#         rospy.spin()
#     except KeyboardInterrupt:
#         sys.exit()

if __name__ == '__main__':
    args = rospy.myargv()[1:]
    #get the racecar name so we know what to subscribe to
    racecar_name=args[0]
    print(racecar_name)
    #IO.initGPIO(100,0,0)#Initialize the GPIO pins
    #IO.beginGettingSpeed()#Initialize the opto-coupler to get code
    #IO.changeDutyCycle((15, 15))
    #time.sleep(2)
    aa=Actuation(racecar_name)
    try:
        rospy.init_node('Actuation_Node', anonymous=True)
        rospy.Subscriber(aa.image_topic, drive_param, aa.callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()
