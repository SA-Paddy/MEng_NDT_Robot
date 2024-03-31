from niryo_one_tcp_client import *
import Coordinate_Script
import Phased_Instructions
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import math

# Here I am just creating a list that holds the updated test data
updated_test_data = []

# Determine the correct IP Address for the Niryo Robot an insert in the quotes
robot_ip_address = input("Please enter the IP address of your robot: ", )

# Create an object called robot defining the NiryoOne robot
# From here on out we can just refer to this object as robot
robot = NiryoOneClient()

# Define the sleep position - this is the position we send the robot into when we are done
sleep_joints = [0.0, 0.55, -1.2, 0.0, 0.0, 0.0]

# Create an object that we can use for error handling if the robot cant connect
robot_connected = False

# Attempt the connection, calibration and set-up sequence with the robot
try:

    # Connect to the robot
    robot.connect(robot_ip_address)

    # Calibrate the robot if required
    robot.calibrate(CalibrateMode.AUTO)

    # Here we need to run the code to ensure the linear  rail is in the start position
    print('You still havent written the starting code to ensure linear rail is at start')

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
    pose_at_start = robot.get_pose()

    robot_connected = True

except Exception as e:
    print("failed to connect: ", e)

# We should ask the user if they want to abort in the event that the robot connection
# Was unsuccessful
if not robot_connected:
    # Ask the user for a yes/no response
    continue_response = input("Do you want to continue (yes/no): ", )
    # Any response other than yes in lowercase will result in the program aborting
    if continue_response != "yes":
        print("Aborting Script")
        exit()

# Call and run the coordinates script - taking the output for our testing coordinates
coordinates = Coordinate_Script.main()

# THIS SPACE IS FOR CALLING OUR RELEVANT PROGRAMS
if robot_connected:
    # Our program is subdivided into 5 sections or phases currently
    # Run the first phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Mov_One()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_One_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here you need to run the first instruction to move the linear rail
    print('You still havent written the linear rail run code')

    # Run the second phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Mov_One()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_Two_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here  you need to run the second instruction to move the linear rail
    print('You still havent written the linear rail run code')

else:
    pass


if robot_connected:

    # This is now the end of the code
    # So we send the robot to the sleep_joints position
    robot.move_joints(*sleep_joints)

    # We set learning mode to true (this is what basically releases the torque in the motors)
    robot.set_learning_mode(True)

    # We disconnect from the robot
    robot.quit()
else:
    pass

# Although the robot has cone to sleep
# We still need to return the linear rail
# The following code should handle this
print('You still havent written the code to return the linear rail to its start position')
