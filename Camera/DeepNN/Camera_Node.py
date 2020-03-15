#!/usr/bin/env python

import sys
import os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def preprocess(img):
   # image = image[100:239,0:319]
    img = cv2.resize(img, (200, 66))
    #img = img / 255.
    return img

#define a camera ros node
#capture the fames from the camera
#publish the frames to a buffer
def Camera(cap,x):
    rospy.init_node('Camera_Node', disable_signals=True)
    pub = rospy.Publisher('sensor_msgs/Image', Image, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    bridge = CvBridge()
    try:
        while not rospy.is_shutdown():
            ret, frame = cap.read()
            image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            pub.publish(image)
            print("publishing image %s" %rospy.get_time())
            rate.sleep()
    except KeyboardInterrupt:
        cap.release()
        sys.exit()

    cap.release()
    sys.exit()



if __name__ == '__main__':
    #cap = Webcam.configureCamera(320,240,30)
    x = 100
    cap = cv2.VideoCapture(-1)
    cap.set(3,320)
    cap.set(4,240)
    cap.set(5,30)
    cap.set(12,100)
    Camera(cap,x)
