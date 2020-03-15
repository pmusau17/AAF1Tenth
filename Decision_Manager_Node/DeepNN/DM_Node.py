#!/usr/bin/env python

import sys
import os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from queue import Queue
bridge = CvBridge()
import message_filters


def callback(steeringNN,RLdata):
    print(RLdata)
    w1,w2,acc,steeringSS,laneDetection = RLdata.data.split()
    print(steeringNN)
    LECsteer = steeringNN.data
    #LECsteer = str(LECsteer)
    print(LECsteer)
    w1 = float(w1)
    w2 = float(w2)
    LECsteer = float(LECsteer)
    steeringSS = float(steeringSS)
    print(w1)
    print(w2)
    print(steeringSS)
    steering = w1*steeringSS + w2*LECsteer
    print(steering)

def DecisionManager():
    try:
        rospy.init_node('DM_Node')
        LECdata = message_filters.Subscriber('steeringNN', String)
        RL_data = message_filters.Subscriber('RLdata', String)
        ts = message_filters.ApproximateTimeSynchronizer([LECdata, RL_data], 10, 0.1, allow_headerless=True)
        ts.registerCallback(callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    DecisionManager()
