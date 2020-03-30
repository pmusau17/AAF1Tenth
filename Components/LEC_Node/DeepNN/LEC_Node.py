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
from deepnncar_components.msg import drive_param
from deepnncar_components.msg import angle_msg

miny=10
maxy=20

class LEC_Node:

    #define the constructor
    def __init__(self,racecar_name,model,height,width):
        self.cv_bridge=CvBridge()
        self.image_topic= '/' + str(racecar_name) +'/Image'
        self.model=load_model(model)
        self.pub=rospy.Publisher('/'+ str(racecar_name) +'/angle_msg',angle_msg, queue_size=1)


    #image callback
    def image_callback(self,data):

        frame = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        img = cv2.resize(frame, (200, 66))
        img = img / 255.
        steer_val = self.nncontroller(img, model)
        steering = self.denormalization(steer_val)
        steeringNN = float("{0:.2f}".format(steering))
        #print(str(steeringNN))
        msg=angle_msg()
        msg.header.stamp=rospy.Time.now()
        msg.steering_angle = steeringNN
        self.pub.publish(msg)

    def nncontroller(self, img, model):
        inputs = np.array(img)[np.newaxis]
        with graph.as_default():
            outputs = self.model.predict(inputs, batch_size=1)
        return float(outputs[0][0])

    def denormalization(self, steer):
        global maxy,miny
        return (float(steer)*(maxy-miny))+miny

if __name__=='__main__':
    rospy.init_node("ros_daev_node",anonymous=True)
    #get the arguments passed from the launch file
    args = rospy.myargv()[1:]
    #get the racecar name so we know what to subscribe to
    racecar_name=args[0]
    print(racecar_name)
    #get the keras model
    load_path_root= rospkg.RosPack().get_path('deepnncar_components')+ '/src/'
    print(load_path_root)
    model = load_path_root+ 'weights.best.hdf5'
    print(model)
    il=LEC_Node(racecar_name,model,66,200)
    image_sub=rospy.Subscriber(il.image_topic,Image,il.image_callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")
        cv2.destroyAllWindows()
