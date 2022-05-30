#!/usr/bin/env python3
import rospy
import math
# ros msg that deals with moving the robot
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan  # ros msg that gets the laser scans
from std_msgs.msg import Bool, Float32
import sys

pose=None
min_dist=1000
def cb(msg):
    global pose, min_dist
    tile_x = float(sys.argv[1])
    tile_y = float(sys.argv[2])
    tile_z = float(sys.argv[3])
    pose=msg
    #print(msg)
    dist = math.sqrt( math.pow((msg.pose.position.x - tile_x),2) + math.pow((msg.pose.position.y - tile_y),2) + math.pow((msg.pose.position.z - tile_z),2) )
    if min_dist > dist:
        min_dist = dist
        print(min_dist)
    if msg.pose.position.z < 1.0:
        exit(0)

rospy.init_node('listener_test', anonymous=True)
rospy.sleep(1)
rospy.wait_for_message("/red/uav_magnet/gain", Float32)
rospy.Subscriber("/red/ball/pose", PoseStamped, cb)
rospy.sleep(0.5)
while pose.pose.position.z > 1.5:
    rospy.sleep(0.2)

points = 35 * math.exp(-0.5*min_dist)
print('Points for ball accuracy: ', points)

