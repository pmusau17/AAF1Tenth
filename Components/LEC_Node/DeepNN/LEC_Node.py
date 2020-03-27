#!/usr/bin/env python2.7
import sys
import os
import numpy as np
import tensorflow as tf
import keras
from keras.models import model_from_json
#from tensorflow.python.keras.models import load_model
from keras.models import load_model
from std_msgs.msg import Float32
#import tensorflow.keras.backend as K
from keras import backend as K
import math
import cv2
import csv
#import model
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()
import rospkg
global graph
graph = tf.get_default_graph()

miny=10
maxy=20
#speed=0

def callback(data):
    frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    img = cv2.resize(frame, (200, 66))
    img = img / 255.
    steer_val = nncontroller(img, model)
    steering = denormalization(steer_val)
    steeringNN = float("{0:.2f}".format(steering))
    #print(str(steeringNN))
    pub = rospy.Publisher('steer',Float32, queue_size=1)
    pub.publish(steeringNN)

def nncontroller(img, model):
    inputs = np.array(img)[np.newaxis]
    with graph.as_default():
        outputs = model.predict(inputs, batch_size=1)
    #K.clear_session()
    return float(outputs[0][0])

def denormalization(steer):
    global maxy,miny
    return (float(steer)*(maxy-miny))+miny

if __name__ == '__main__':
    load_path_root= rospkg.RosPack().get_path('deepnncar_components')+ '/src/'
    print(load_path_root)
    filename = load_path_root+ 'weights.best.hdf5'
    print(filename)
    model = load_model(filename)
    print("loaded model")
    rospy.init_node('LEC_Node',anonymous=True)
    speed_data=rospy.Subscriber('speed', Float32)
    rospy.Subscriber('Image',Image,callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        sys.exit()
