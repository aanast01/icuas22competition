#icuas 22 competition 
#script for manually go back in zone 0
#auth: Anastasiou Andreas
#date: February 2022
import sys
import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32
from std_srvs.srv import Empty

dronePose = PoseStamped()
flag_odom = False

def pose_callback(pose):
	global dronePos,flag_odom
	dronePos = pose
	if pose.pose.position.z>7.9:
		flag_odom=True

def main(x,y,z,spawn_ball):
	try:	
		global dronePos,flag_odom
		rospy.init_node('testingNode', anonymous=True)
		posePub = rospy.Publisher('/red/tracker/input_pose', PoseStamped, queue_size=10)
		ballRelease = rospy.Publisher('/red/ball/magnet/gain', Float32, queue_size=10)
		ballSpawn = rospy.ServiceProxy('/red/spawn_ball', Empty)
		rospy.Subscriber("/red/pose", PoseStamped, pose_callback)
		rospy.sleep(1)
		
			
		pos0 = PoseStamped()
		pos0.pose.position.x = float(x)
		pos0.pose.position.y = float(y)
		pos0.pose.position.z = float(z)
		
		pos1 = PoseStamped()
		pos1.pose.position.x = float(x)
		pos1.pose.position.y = float(y)
		pos1.pose.position.z = 8
		
		
		pos2 = PoseStamped()
		pos2.pose.position.x = dronePos.pose.position.x
		pos2.pose.position.y = dronePos.pose.position.y
		pos2.pose.position.z = 8
		
		posePub.publish(pos2)
		flag_odom=False
		while not flag_odom:
			rospy.sleep(0.4)
		print('increasing altitude')
		#rospy.sleep(4)
		posePub.publish(pos1)
		print('go home')
		rospy.sleep(5)
		posePub.publish(pos0)
		print('lower altitude')
		rospy.sleep(3)
		if(spawn_ball):
			print('spawning ball ', spawn_ball)
			ballRelease.publish(1.0)
			rospy.sleep(1.5)
			ballSpawn.call()
	except Exception as e:
		print(e)


if __name__ == "__main__":
	if (len(sys.argv)<5):
		print('please enter home x,y,z and flag for spawning the ball')
		exit()
	else:
		print('home position: ', sys.argv[1], sys.argv[2], sys.argv[3], ' spawn ball: ', sys.argv[4])
		main(sys.argv[1], sys.argv[2], sys.argv[3], bool(int(sys.argv[4])))
