#!/usr/bin/env python3
import rospy
import math
# ros msg that deals with moving the robot
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan  # ros msg that gets the laser scans
from std_msgs.msg import Bool, Float32


rospy.init_node('listener_test', anonymous=True)
rospy.sleep(0.5)
print('waiting for start flag')
rospy.wait_for_message("/red/challenge_started", Bool)
start = rospy.get_rostime()
#rospy.sleep(1)
print('waiting for ball release')
rospy.wait_for_message("/red/uav_magnet/gain", Float32)
finish = rospy.get_rostime()
time = float(str((finish-start)/1000000000))
print(time)
points = 40 * math.exp(-time/100)
print('Points for time: ',points)
