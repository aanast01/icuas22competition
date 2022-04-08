#icuas 22 competition 
#script for manually traversing in the given area
#auth: Anastasiou Andreas
#date: February 2022

import rospy
from trajectory_msgs.msg import MultiDOFJointTrajectory,MultiDOFJointTrajectoryPoint
from geometry_msgs.msg import Transform, Twist
from std_msgs.msg import Float32
from std_srvs.srv import Empty

try:
	rospy.init_node('testingNode', anonymous=True)
	posePub = rospy.Publisher('/red/tracker/input_trajectory', MultiDOFJointTrajectory, queue_size=10)
	ballRelease = rospy.Publisher('/red/ball/magnet/gain', Float32, queue_size=10)
	ballSpawn = rospy.ServiceProxy('/red/spawn_ball', Empty)
	rospy.sleep(1)
	
	trajectory = MultiDOFJointTrajectory()
	trajectory.joint_names = ['pos0', 'pos1', 'pos2','pos3', 'pos4', 'pos5','pos6', 'pos7']
	
	point = MultiDOFJointTrajectoryPoint()
	trsfrm = Transform()
	trsfrm.translation.x = -10
	trsfrm.translation.y = 1
	trsfrm.translation.z = 3
	point.transforms.append(trsfrm)
	
	trsfrm.translation.x = 0
	trsfrm.translation.y = 0
	trsfrm.translation.z = 4
	point.transforms.append(trsfrm)
	trajectory.points.append(point)
	
	point = MultiDOFJointTrajectoryPoint()
	trsfrm.translation.x = 0
	trsfrm.translation.y = 0
	trsfrm.translation.z = 4
	point.transforms.append(trsfrm)
	
	trsfrm.translation.x = 5
	trsfrm.translation.y = -1
	trsfrm.translation.z = 4.5
	point.transforms.append(trsfrm)
	
	trsfrm.translation.x = 10
	trsfrm.translation.y = -3
	trsfrm.translation.z = 5
	point.velocities.append(Twist())
	point.velocities.append(Twist())
	twst = Twist()
	twst.linear.x=5
	point.velocities.append(twst)
	point.transforms.append(trsfrm)
	trajectory.points.append(point)
	
	posePub.publish(trajectory)
	rospy.sleep(6.3)
	print('Releasing Ball...')
	ballRelease.publish(0.0)
	rospy.sleep(1)
	ballRelease.publish(1.0)
	print('Going Back')
	trajectory = MultiDOFJointTrajectory()
	trajectory.joint_names = ['pos0', 'pos1', 'pos2','pos3', 'pos4', 'pos5','pos6', 'pos7']
	
	point = MultiDOFJointTrajectoryPoint()
	trsfrm.translation.x = 9
	trsfrm.translation.y = -3
	trsfrm.translation.z = 5
	point.transforms.append(trsfrm)
	
	trsfrm.translation.x = 0
	trsfrm.translation.y = -1
	trsfrm.translation.z = 4
	point.transforms.append(trsfrm)
	
	trsfrm.translation.x = -9
	trsfrm.translation.y = 0.5
	trsfrm.translation.z = 4
	point.transforms.append(trsfrm)
	trajectory.points.append(point)	
	posePub.publish(trajectory)
	rospy.sleep(6)
	print('Done! Spawning new ball')
	ballSpawn.call()
	print('New Ball Spawned!\nExiting...')
except Exception as e:
	print(e)
	
	
