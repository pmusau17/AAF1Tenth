#!/usr/bin/env python2.7
import sys
import os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def preprocess(img):
    img = cv2.resize(img, (200, 66))
    return img

#define a camera ros node
#capture the fames from the camera
#publish the frames to a buffer
def Camera(cap,racecar_name):
    rospy.init_node('Camera_Node', disable_signals=True)
    pub = rospy.Publisher('/'+ racecar_name+ '/Image', Image, queue_size=1)
    rate = rospy.Rate(40) # 10hz
    bridge = CvBridge()
    try:
        while not rospy.is_shutdown():
            ret, frame = cap.read()
            image = bridge.cv2_to_imgmsg(frame, encoding="passthrough")
            pub.publish(image)
            #print("publishing image %s" %rospy.get_time())
            rate.sleep()
    except KeyboardInterrupt:
        cap.release()
        sys.exit()
    cap.release()
    sys.exit()

if __name__ == '__main__':
    args = rospy.myargv()[1:]
    racecar_name=args[0]
    cap = cv2.VideoCapture(-1)
    cap.set(3,320)
    cap.set(4,240)
    cap.set(5,10)
    cap.set(12,100)
    Camera(cap,racecar_name)
