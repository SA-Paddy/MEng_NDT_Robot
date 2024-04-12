# NDT Robot Testing Script
# Please ensure you have installed Numpy as well as having cloned the GitHub directory (git clone web address):
# https://github.com/LSBU-Electronics-Lab/ApiTCP_Python_NiryoOne.git
# The GitHub Library needs to be set as a Root Folder
# If you go into the Python Terminal (down the bottom of this screen) and put in the following commands:
# pip install numpy
# This will install numpy
# git clone https://github.com/LSBU-Electronics-Lab/ApiTCP_Python_NiryoOne.git
# This will install the NiryoOne relevant API as a folder set in the project
# The folder set is called ApiTCP_Python_NiryoOne
# Right-click on the folder set - navigate to "mark directory as" and set this to Sources Root


# Import the relevant libraries - this is just telling the interpreter where to look for certain functions
# niryo_one_tcp_client is the API for the NiryoOne Robots being used in LSBU currently
# Matplotlib is the matlab 2D graphical plotter for  representation of  data
# Numpy is an efficient mathematical scientific computing library. Good for arrays and matrices
# math is a python module granting access to a very wide variety of mathematical functions
from niryo_one_tcp_client import *

# Determine the correct IP Address for the Niryo Robot an insert in the quotes
robot_ip_address = "192.168.1.106"

# Create an object called robot defining the NiryoOne robot
# From here on out we can just refer to this object as robot
robot = NiryoOneClient()

# Connect to the robot
robot.connect(robot_ip_address)

# Set the tool being used (if required - this will probably get commented out in the final version)
gripper_used = RobotTool.GRIPPER_2

# Define the sleep position - this is the position we send the robot into when we are done
sleep_joints = [0.0, 0.55, -1.2, 0.0, 0.0, 0.0]

# Calibrate the robot if required
robot.calibrate(CalibrateMode.AUTO)

# First lets make sure that we are starting from the sleep position
# In the first instance we get the current joint angles for all 6 joints
# We place this information in an object we call joints_start
joints_start = robot.get_joints()

# The request returns a two part list formatted as [True, [j1, j2, j3, j4, j5, j6]]
# This is pretty useless to us as we cant undertake comparative analysis
# We need to pull just the joint angles out
# We will place the joint angles in an object called joints_start_list
# joints_start_list will have the following formatting [j1, j2, j3, j4, j5, j6]
joints_start_list = joints_start[1]

# Now we undertake the comparative analysis to check if we are starting from the sleep position
# this code effectively says that if the joints_start_list does not match sleep_joints then do the attributed action
if joints_start_list != sleep_joints:

    # The attributed action is to move the robot to the position defined by sleep_joints
    robot.move_joints(*sleep_joints)

    # The following just tells the interpreter to pass by this code if joints_start_list was a match to sleep_joints
else:
    pass

# All we are doing here is saving the starting real coordinates to an object incase we need it later
pose_start = robot.get_pose()


# Define the first function that can be called
# I am calling this function NDT1()
def ndt1():
    # We already know we are starting from the sleeping pose
    # I will now move the end effector (the TCP) to the following cartesian (real world) point
    # Note that the x, y & z values are provided in metres
    # The roll, pitch and yaw are provided in radians

    #robot.move_pose(-.0, -0.2, 0.23, -0.052, 0.715, -1.563)
    my_joints = robot.get_joints()
    robot.move_joints(-1.56367106511, -0.248965312548, -0.609601007311, -0.00153588974176, 0.18, -1.563)
    my_position = robot.get_pose()
    print(my_position)

    # Because this is a test code - I want to see the impact of every alteration I make
    # I have therefore included the following which needs me to hit the enter button before it will continue
    # Note - If running the program from Pycharm - you need to click on the Python run window
    # where it asks you if you want to continue - before you hit enter - otherwise you will just place a hard return
    # inside the code here
    #input("press enter to continue")
    #print("continuing")

    # Now as per my video - having extended the arm out to my first pose
    # I now wanted to rotate it - to do so, I need to move from a cartesian space command to a joints space command
    # Using the same trick as above I first get the current joint information
    joints1 = robot.get_joints()

    # The request returns a two part list formatted as [True, [j1, j2, j3, j4, j5, j6]]
    # This list is pretty useless again, so we need to extract just the angles element
    joints_list1 = joints1[1]

    # Here we are printing the joint angles (in radians) in the python run console just for information purposes
    #print("joints list:", joints_list1)

    # Putting in a user input to continue if we are happy
    #input("press enter to continue")
    #print("continuing")

    # Within our object joints_list1 we are replacing the first angle with a number of our choice (in radians)
    # This will rotate the robot about the base
    # A negative value will rotate clockwise
    # A positive value will rotate anti-clockwise
    # We have found that maximum rotation is 3 radians (just shy of pi)
    #joints_list1[0] = 3

    # Now we move the robot in joints space, assigning the value of each joint from our list
    # lists always start with the first value being list position 0
    #robot.move_joints(joints_list1[0], joints_list1[1], joints_list1[2], joints_list1[3], joints_list1[4],
                      # joints_list1[5])

    # Now I haven't tested this yet - but we should theoretically be able to achieve this last line of code
    # In a simpler fashion just by using:
    # robot.move_joints(*joints_list1)

    # Putting in a user input to continue if we are happy
    #input("press enter to continue")
    #print("continuing")

    # Now I am just getting this set of coordinates and checking that it outputs the relevant real world values
    #pose2 = robot.get_pose()
    #print("pose 2:", pose2)

    # There is nothing to return - so we are just closing the function at this point
    return


# to run the NDT() program we just call the defined function
ndt1()

# This is now the end of the code for the time being
# So we send the robot to the sleep_joints position
robot.move_joints(*sleep_joints)

# We set learning mode to true (this is what basically releases the torque in the motors)
robot.set_learning_mode(True)

# We disconnect from the robot
robot.quit()
