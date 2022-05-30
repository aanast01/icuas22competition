#!/usr/bin/env python3
import rospy
import math
# ros msg that deals with moving the robot
from geometry_msgs.msg import Twist, PoseStamped, Point
from sensor_msgs.msg import LaserScan  # ros msg that gets the laser scans
from std_msgs.msg import Bool, Float32
import sys

rospy.init_node('listener_test', anonymous=True)
rospy.sleep(1)
tag_pose = rospy.wait_for_message("/red/tag_position_reconstructed", Point)
tile_x = float(sys.argv[1])
tile_y = float(sys.argv[2])
tile_z = float(sys.argv[3])

dist = math.sqrt( math.pow((tag_pose.x - tile_x),2) + math.pow((tag_pose.y - tile_y),2) + math.pow((tag_pose.z - tile_z),2) )
print(dist)

points = 25 * math.exp(-2*dist)
print('Points for tag reconstraction: ', points)
