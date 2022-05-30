#!/usr/bin/env python3

import rospy
import time
from math import sqrt
#from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, Bool
from rosgraph_msgs.msg import Clock
data = Odometry()
sec = 0

class OdometryModifier:
  def __init__(self):
    rospy.init_node('odom_drone', anonymous=True)
    rospy.wait_for_message("/red/challenge_started", Bool)
    self.sub = rospy.Subscriber("/red/odometry", Odometry, self.callback)
    self.bat = rospy.Subscriber("/clock", Clock, self.sec_cb)
    self.pub = rospy.Publisher('odom2', Odometry, queue_size=10)

    self.total_distance = 0.
    self.previous_x = 0
    self.previous_y = 0
    self.first_run = True
       
  def sec_cb(self, dat):
      global sec
      sec = dat.clock.secs
      
  def checker(self):
    global data
    l1 = [data.twist.twist.linear.x, data.twist.twist.linear.y, data.twist.twist.angular.x, data.twist.twist.angular.y]
    time.sleep(5)
    l2 = [data.twist.twist.linear.x, data.twist.twist.linear.y, data.twist.twist.angular.x, data.twist.twist.angular.y]
    
    if l1==l2:
        avg_spd = (self.total_distance/sec)
        print ("average speed: {:.2f}m/s".format(avg_spd))
        rospy.signal_shutdown("Done Calculating the average speed") 
      
  def callback(self, data):
    if(self.first_run):
      self.previous_x = data.pose.pose.position.x
      self.previous_y = data.pose.pose.position.y
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    d_increment = sqrt((x - self.previous_x) * (x - self.previous_x) + (y - self.previous_y) * (y - self.previous_y))
    self.total_distance = self.total_distance + d_increment
    print("Total distance traveled is {:.2f}m".format(self.total_distance))
    self.pub.publish(data)
    self.previous_x = data.pose.pose.position.x
    self.previous_y = data.pose.pose.position.y
    self.first_run = False
    
    if abs(data.twist.twist.linear.x) <= 0.0051 and abs(data.twist.twist.linear.y) <= 0.0051 and abs(data.twist.twist.angular.x) <= 0.0051 and abs(data.twist.twist.angular.y) <= 0.0051:
        self.checker() 

if __name__ == '__main__':
  try:
    #odom = 
    OdometryModifier()
    rospy.spin()
  except:
    print("exit")
