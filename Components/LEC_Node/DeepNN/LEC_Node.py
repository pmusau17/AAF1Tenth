#!/usr/bin/env python

import sys
import os
import numpy as np
import tensorflow as tf
import math
import cv2
import csv
import model
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()

miny=10
maxy=20
speed=0


def preprocess(img):
    img = cv2.resize(img, (200, 66))
    return img

def denormalization(steer):
    global maxy,miny
    return (float(steer)*(maxy-miny))+miny

def join(dirpath, filename):
    return os.path.join(dirpath, filename)

#defining the tensorflow model to be global
sess = tf.InteractiveSession()
saver = tf.train.Saver()
model_name = 'test.ckpt'
save_dir = os.path.abspath('/home/scope/catkin_ws/src/ros_trial/AutonomousDriving/model_lab')
model_path = join(save_dir, model_name)
saver.restore(sess, model_path)

def publisher(steeringNN):
    pub = rospy.Publisher('steeringNN',String, queue_size=1)
    pub.publish("%s"%str(steeringNN))
    print(steeringNN)

def callback(data):
    global sess,model
    frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    frame = preprocess(frame)
    with sess.as_default():
        steer = model.y.eval(feed_dict={model.x: [frame]})[0][0]
    steering = denormalization(steer)
    steeringNN = float("{0:.2f}".format(steering))
    #print(steeringNN)
    publisher(steeringNN)


def autonomousDriving():
    try:
        rospy.init_node('LEC_Node')
        rospy.Subscriber('Buffer_Image', Image, callback)
        rospy.spin()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    autonomousDriving()
