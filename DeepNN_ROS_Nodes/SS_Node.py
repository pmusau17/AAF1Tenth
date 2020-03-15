#!/usr/bin/env python

import sys
import os
import numpy as np
import math
import cv2
import model
import SafetyManagerAutonomousClient
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()


def publish(steeringSS,laneDetection):
    pub = rospy.Publisher('steeringSS', String, queue_size=1)
    SS_data = ("%s %s" %(str(steeringSS),str(laneDetection)))
    print(SS_data)
    pub.publish(SS_data)

def callback(data):
    global bridge
    laneDetection,blur,steeringSS = SafetyManagerAutonomousClient.runSafetyManager(data)
    #print(steeringSS)
    publish(steeringSS,laneDetection)

def LaneDetection():
    try:
        rospy.init_node('SS_Node')
        rospy.Subscriber('Buffer_Image', Image, callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    LaneDetection()
