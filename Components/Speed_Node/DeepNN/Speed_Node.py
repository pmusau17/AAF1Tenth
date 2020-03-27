#!/usr/bin/env python2.7
import sys
import os
import base64
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
#import IO
import time

def Speed():
    rospy.init_node('Speed_Node', anonymous=True)
    pub = rospy.Publisher('speed', Float32, queue_size=1)
    rate = rospy.Rate(40) # 10hz
    try:
        while not rospy.is_shutdown():
            speed_value = 1.0          #IO.speed
            #speed = float("{0:.2f}".format(speed))
            pub.publish(speed_value)
            #print(str(speed_value))
            #print("publishing speed %s" %rospy.get_time())
            rate.sleep()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    #IO.initGPIO(100,0,0)#Initialize the GPIO pins
    #IO.beginGettingSpeed()#Initialize the opto-coupler to get code
    #IO.changeDutyCycle((15, 15))
    #time.sleep(2)
    Speed()
