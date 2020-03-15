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

def publish(frame):
    pub = rospy.Publisher('Buffer_Image', Image, queue_size=1)
    pub.publish(frame)

def callback(data):
    global bridge
    image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    publish(data)
    #cv2.imshow("Image window", image)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #cap.release()
        #cv2.destroyAllWindows()

def Buffer():
    try:
        rospy.init_node('Buffer_Node',disable_signals=True)
        rospy.Subscriber('Image', Image, callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    Buffer()
