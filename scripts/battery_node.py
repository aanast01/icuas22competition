#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, Empty
from time import sleep
from std_srvs.srv import Empty as nil
from geometry_msgs.msg import Twist


def talker():
    pub = rospy.Publisher('battery_level', Float32, queue_size=10)
    vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('battery', anonymous=True)
    
    x = 100.00000000
    
    while not rospy.is_shutdown():
        x = x - 0.0010000
        rate = rospy.Rate(10) # 10hz
        pub.publish(x)
        rate.sleep()
        if x <= 5:
            twist = Twist()
            twist.linear.z = -15
            land = rospy.Publisher('/quadcopter_land', Empty, queue_size=1)
            srv=rospy.ServiceProxy('/shutdown',nil)
            vel.publish(twist)
            sleep(3)
            land.publish()
            sleep(4)
            service_example=srv()
            sleep(0.5)
            break
        
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
