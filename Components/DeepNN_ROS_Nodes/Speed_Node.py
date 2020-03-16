#!/usr/bin/env python

import sys
import os
import cv2
import Webcam
import base64
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
import IO
import time


def Speed():
    rospy.init_node('Speed_Node', disable_signals=True)
    pub = rospy.Publisher('Speed', Float32, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    try:
        while not rospy.is_shutdown():
            speed = IO.speed
            speed = float("{0:.2f}".format(speed))
            pub.publish(speed)
            print("publishing image %s" %rospy.get_time())
            rate.sleep()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    IO.initGPIO(100,0,0)#Initialize the GPIO pins
    IO.beginGettingSpeed()#Initialize the opto-coupler to get code
    IO.changeDutyCycle((15, 15))
    time.sleep(2)
    Speed()
