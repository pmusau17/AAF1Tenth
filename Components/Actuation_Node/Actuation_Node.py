#!/usr/bin/env python2.7
import sys
import os
import numpy as np
import math
import cv2
import rospy
#import IO
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()


def callback(actuation_data):
    #print(actuation_data)
    w1, steering_pwm, w2, speed_pwm = actuation_data.data.split( )
    #IO.changeDutyCycle((steering_pwm, speed_pwm))
    print("speed:%s steer:%s"%(speed_pwm,steering_pwm))

def Actuation():
    try:
        rospy.init_node('Actuation_Node', anonymous=True)
        rospy.Subscriber('drive_parameters', String, callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    #IO.initGPIO(100,0,0)#Initialize the GPIO pins
    #IO.beginGettingSpeed()#Initialize the opto-coupler to get code
    #IO.changeDutyCycle((15, 15))
    #time.sleep(2)
    Actuation()
