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
from message_filters import ApproximateTimeSynchronizer, Subscriber
from deepnncar_components.msg import drive_param
from deepnncar_components.msg import velocity_msg
from deepnncar_components.msg import angle_msg
from deepnncar_components.msg import drive_param

class DecisionManager:
    def __init__(self,racecar_name):
        self.racecar_name=racecar_name
        #subscribe to the angle and the speed message
        self.angle_sub=Subscriber('/'+self.racecar_name+'/angle_msg',angle_msg)
        self.velocity_sub=Subscriber('/'+self.racecar_name+'/velocity_msg',velocity_msg)
        self.pub=rospy.Publisher(self.racecar_name+'/drive_parameters',drive_param,queue_size=20)

        #create the time synchronizer
        self.sub = ApproximateTimeSynchronizer([self.angle_sub,self.velocity_sub], queue_size = 20, slop = 0.019, allow_headerless=True)
        #register the callback to the synchronizer
        self.sub.registerCallback(self.master_callback)

    def master_callback(self,angle_msg,velocity_msg):
        msg=drive_param()
        msg.header.stamp=rospy.Time.now()
        msg.angle=angle_msg.steering_angle
        msg.velocity=velocity_msg.velocity
        self.pub.publish(msg)

if __name__ == '__main__':
    #DecisionManager()
    #get the arguments passed from the launch file
    args = rospy.myargv()[1:]
    racecar_name=args[0]
    dm = DecisionManager(racecar_name)
    rospy.init_node('decision_manager_'+racecar_name, anonymous=True)
    rospy.spin()
