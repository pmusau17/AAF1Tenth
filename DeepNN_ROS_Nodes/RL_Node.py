#!/usr/bin/env python

import sys
import os
import cv2
import Webcam
import base64
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from queue import Queue
bridge = CvBridge()
import RLCar
import pickle

w1 = 0.5
w2 = 0.5
acc = 15.58

def publisher(w1,w2,acc,steeringSS,laneDetection):
    pub = rospy.Publisher('RLdata', String, queue_size=1)
    RLdata = ("%s %s %s %s %s" %(str(w1),str(w2),str(acc),str(steeringSS),str(laneDetection)))
    pub.publish(RLdata)

def callback(data,Qtable,explore,exploration_steps):
    global w1,w2,acc
    steeringSS, laneDetection = data.data.split()
    acc = round(acc,4)
    laneDetection = int(laneDetection)
    w1,w2,acc = RLCar.run(acc,laneDetection,w1,w2,exploration_steps,explore,Qtable)
    publisher(w1,w2,acc,steeringSS,laneDetection)
    print("w1:%f w2:%f"%(w1,w2))

def RLAgent(Qtable,explore,exploration_steps):
    try:
        rospy.init_node('RL_Node')
        callback_lambda = lambda data: callback(data,Qtable,explore,exploration_steps)
        rospy.Subscriber('steeringSS', String, callback_lambda)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    explore = "0"
    exploration_steps = 500
    if(explore == "0"):
        Qtable = RLCar.initQTable()
    elif(explore == "1"):
        Qtable = RLCar.pickletable()
    RLAgent(Qtable,explore,exploration_steps)
