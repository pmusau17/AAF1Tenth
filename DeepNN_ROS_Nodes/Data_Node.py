#!/usr/bin/env python
import rosbag
from std_msgs.msg import Int32, String

bag = rosbag.Bag('data.bag', 'w')

try:
    s = String()
    s.data = 'foo'

    #i = Int32()
    #i.data = 42

    bag.write('steeringNN', s)
    #bag.write('numbers', i)
finally:
    bag.close()
