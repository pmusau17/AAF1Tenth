#!/usr/bin/env python2.7
import sys
import os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge, CvBridgeError
from queue import Queue
bridge = CvBridge()
import message_filters

def callback(steer,speed):
    print(steer)
    print(speed)
    pub = rospy.Publisher('drive_parameters', String, queue_size=1)
    msg = ("%s %s" %(str(steer),str(speed)))
    pub.publish(msg)

def DecisionManager():
    try:
        rospy.init_node('DM_Node', anonymous=True)
        steer_data = message_filters.Subscriber('steer', Float32, queue_size=1)
        speed_data = message_filters.Subscriber('speed', Float32, queue_size=1)
        ts = message_filters.ApproximateTimeSynchronizer([steer_data, speed_data], queue_size = 10, slop = 0.019, allow_headerless=True)              #10, 0.1, allow_headerless=True)
        ts.registerCallback(callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    DecisionManager()
