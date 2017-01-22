#!/usr/bin/env python

"""
  Contains commands for controlling the movement of the robot based on the speech input given. 

  Modified by dbha974@cse.unsw.edu.au
"""

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from std_msgs.msg import String
from math import copysign

class VoiceNav:
    pub = None
    def __init__(self):
        rospy.init_node('voice_nav')
        
        rospy.on_shutdown(self.cleanup)
      	
	# We don't have to run the script very fast
        self.rate = rospy.get_param("~rate", 5)
        r = rospy.Rate(self.rate)
	ratezz = rospy.Rate(10)
        
        # A flag to determine whether or not voice control is paused
        self.paused = False
        global pub
        pub = rospy.Publisher('chatter', String, queue_size=10)
        # Publish the Twist message to the cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)

	#tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("wait for the action server to come up")
	#allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

        
        # Subscribe to the /recognizer/output topic to receive voice commands.
        rospy.Subscriber('/recognizer/output', String, self.speech_callback)
        
        # A mapping from keywords or phrases to commands
        self.keywords_to_command = {'stop': ['stop', 'halt', 'abort', 'kill', 'panic', 'off', 'freeze', 'shut down', 'turn off', 'help', 'help me'],
									'kitchen': ['cooking station', 'canteen', 'cookery', 'cookhouse', 'mess'],
									'living room': ['central area', 'drawing room', 'common room', 'front room', 'sitting room'],
									'docking station': ['initial area', 'initial room', 'initial zone', 'base', 'starting zone', 'starting room', 'starting zone', 'recharge',],
									'identify': ['dig up', 'find out where', 'uncover the', 'track down', 'search for', 'identify'],
                                    'slower': ['slow down', 'slower'],
                                    'faster': ['speed up', 'faster'],
                                    'forward': ['forward', 'ahead', 'straight'],
                                    'backward': ['back', 'backward', 'back up'],
                                    'rotate left': ['rotate left'],
                                    'rotate right': ['rotate right'],
                                    'turn left': ['turn left'],
                                    'turn right': ['turn right'],
                                    'quarter': ['quarter speed'],
                                    'half': ['half speed'],
                                    'full': ['full speed'],
                                    'pause': ['pause speech'],
                                    'continue': ['continue speech']}
        
        rospy.loginfo("Ready to receive voice commands")
	
        
                              
    def get_command(self, data):
        # Attempt to match the recognized word or phrase to the 
        # keywords_to_command dictionary and return the appropriate
        # command
        for (command, keywords) in self.keywords_to_command.iteritems():
            for word in keywords:
                if data.find(word) > -1:
                    return command
        
    def speech_callback(self, msg):
        # Get the motion command from the recognized phrase
        command = self.get_command(msg.data)
        
        # Log the command to the screen
        rospy.loginfo("Command: " + str(command))
        
        # If the user has asked to pause/continue voice control,
        # set the flag accordingly 
        if command == 'pause':
            self.paused = True
        elif command == 'continue':
            self.paused = False
        
        # If voice control is paused, simply return without
        # performing any action
        if self.paused:
            return       

	
	#we'll send a goal to the robot to tell it to move to a pose that's near the docking station
	
	#customize the following Point() values so they are appropriate for your location
		
        # The list of if-then statements should be fairly
        # self-explanatory
        waypoints = list()
        p1 = Point(1.05455362797, 0.0144122838974, 0.0)
        p2 = Point(2.458, -0.1085, 0.0)
        p3 = Point(2.7262856903, -1.818253, 0.0)
        p4 = Point(0.3336, -1.88577, 0.0)
        waypoints.append(Pose(p1, Quaternion(0.000, 0.000, 0.0291398, 0.999575)))
        waypoints.append(Pose(p2, Quaternion(0.000, 0.000, -0.717091982035, 0.696978542927)))
        waypoints.append(Pose(p3, Quaternion(0.000, 0.000, -0.999, -0.044129379175)))
        waypoints.append(Pose(p4, Quaternion(0.000, 0.000, 0.9999, -0.000775)))
		#p1 = docking station
		#p2 = living room
		#p3 = kitchen
		#p4 = door

	hello_str = "hello"
        i = 0
        global pub
        if command == 'forward':
            while i < 4 and not rospy.is_shutdown():
                goal = MoveBaseGoal()
	        goal.target_pose.header.frame_id = 'map'
	        goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose = waypoints[i]
                self.move(goal)
                i += 1
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
            #ratezz.sleep()
	elif command == 'backward':
            while i < 3 and not rospy.is_shutdown():
                goal = MoveBaseGoal()
	        goal.target_pose.header.frame_id = 'map'
	        goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose = waypoints[i]
                self.move(goal)
                i += 1
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif command == 'rotate right':  
            while i < 2 and not rospy.is_shutdown():
                goal = MoveBaseGoal()
	        goal.target_pose.header.frame_id = 'map'
	        goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose = waypoints[i]
                self.move(goal)
                i += 1
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
        elif command == 'rotate left':  
            while i < 1 and not rospy.is_shutdown():
                goal = MoveBaseGoal()
	        goal.target_pose.header.frame_id = 'map'
	        goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose = waypoints[i]
                self.move(goal)
                i += 1
            rospy.loginfo(hello_str)
            pub.publish(hello_str) 

        

    def move(self, goal):
	
        #start moving
	self.move_base.send_goal(goal)
	#allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(60))
        if not success:
	        self.move_base.cancel_goal()
		rospy.loginfo("The base failed to reach the desired pose")
	else:
		# We made it!
		state = self.move_base.get_state()
		if state == GoalStatus.SUCCEEDED:
			rospy.loginfo("Hooray, reached the desired pose")
                
    def cleanup(self):
        rospy.sleep(1)

if __name__=="__main__":
    try:
        VoiceNav()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Voice navigation terminated.")

