# We would recommend you run this project through PyCharm.
# PyCharm community is  free to download from their download section on their website
# Import the relevant libraries or python files that will be needed to run this code
# These are needed due to dependencies on them for functions or classes or data processing types
# This whole project runs in a virtual environment - so until it is packaged into an .exe
# We will be required to install some of the packages everytime we look to run on a new computer
# Or everytime we run it on an LSBU computer
# First and foremost navigate to the 'terminal' window at the bottom of PyCharm
# Either copy and paste the following or type it in the terminal window:
# python -m pip install --upgrade pip
# Once the latest pip installer is installed copy or type  the following:
# git clone https://github.com/LSBU-Electronics-Lab/ApiTCP_Python_NiryoOne.git
# This will add a new folder in your project called ApiTCP_Python_NiryoOne
# Right click on this folder, go to the bottom of the menu and mark directory as a sources root
# Expand the ApiTCP_Python_NiryoOne folder and find the sub-folder named niryo_one_tcp_client
# Right click on this folder, go to the bottom of  the menu and mark directory as a sources root
# Next go back to the terminal and type or copy the following
# (for each one - wait for it to finish installing before moving  on to the next):
# pip install numpy
# pip install serial
# pip install seaborn
# pip install pandas
# You may get error messages saying that it could not find a version that satisfies
# If you do - dont stress - this just means that the latest version is already probably installed

# ------------ potential errors
# 1. You may need to update your phased move instructions by passing variables from here to there
# 2. if your coordinate system appears messed up  in your data -
#    it might be due to you not having the get pose argument before adjustment in corrected coordinates
# ------------

from niryo_one_tcp_client import *
import Coordinate_Script
import Phased_Instructions
import Linear_Rail_Instructions
import pandas as pd
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import Menu
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import math

# Here I am just creating a list that holds the updated test data
updated_test_data = []

#hello world

# Create the menu logic objects
t_test_only = None
file_analysis = None

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
    print('You still have yet to written the starting code to ensure linear rail is at start')

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

    # If we have made it this  far in the code without an error then clearly the connection was successful
    robot_connected = True

# All this code does is 'handle errors gracefully'
# Any error is caught in the object e which can then be printed as a  message to aid in debugging
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
    else:
        pass

# Now lets call the menu function
menu_choice = Menu.men()
print(f"Menu Choice: {menu_choice}")

# Menu logic
if menu_choice == 1:
    t_test_only = True
    robot_connected = False
elif menu_choice == 2:
    file_analysis = True
    robot_connected = False
elif menu_choice ==3:
    t_test_only = True
else:
    pass

# I have commented out the following print commands as they are really only used for debugging
# print('t_test_only: ', t_test_only)
# print('file_analysis: ', file_analysis)
# print('robot_connected', robot_connected)

# Create a conditional statement that reacts to the menu choice
if file_analysis == True:
    # Create a Tkinter root window
    root = tk.Tk()
    # I have commented out the following code as I found that hiding the window just made for confusion
    #root.withdraw()

    # Ask the user to select a CSV file using a file dialog
    csv_file = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])

    # Check if the user selected a file
    if not csv_file:
        print("No file selected. Exiting.")
        exit()
    else:
        pass

    # load the CSV data into a panda data frame
    df = pd.read_csv(csv_file)

    # pivot the data to create a 2D array
    heatmap_data = df.pivot(index='y_coordinate', columns='x_coordinate', values='sensor_value')

    # create the heatmap using seaborn
    plt.figure(figsize=(10, 8))
    plt.title('Heatmap of Sensor Data')
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt=".1f", cbar_kws={'label': 'Sensor Values'})

    # output the map
    plt.show()

else:
    pass

# Conditional statement that reacts to the menu choice
if t_test_only == True:

    # Call and run the coordinates script - taking the output for our testing coordinates
    coordinates = Coordinate_Script.main()

else:
    pass


# THIS SPACE IS FOR CALLING OUR RELEVANT PROGRAMS
if robot_connected:

    # Here you need to run the first instruction to move the linear rail to position (0, 325)
    travel_dist_global = 325
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=True)

    # Our program is subdivided into 5 sections or phases currently
    # Run the first phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Move_One()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_One_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here  you need to run the second instruction to move the linear rail to position (0, 650)
    travel_dist_global = 325
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=True)

    # Run the second phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Move_Two()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_Two_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here  you need to run the third instruction to move the linear rail to position (0, 975)
    travel_dist_global = 325
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=True)

    # Run the third phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Move_Three()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_Three_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here  you need to run the fourth instruction to move the linear rail to position (0, 375)
    travel_dist_global = 600
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=False)

    # Run the fourth phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Move_Four()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_Four_Coords_and_Index = (coordinates[last_position_index], last_position_index)

    # Here  you need to run the fifth instruction to move the linear rail to position (0, 600)
    travel_dist_global = 225
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=True)

    # Run the fourth phase and capture the returned data
    updated_test_data, last_position_index = Phased_Instructions.Phase_Move_Five()

    # Lets create a tuple list to store the coordinates and index
    # from the last position - this is for error handling
    Phase_Five_Coords_and_Index = (coordinates[last_position_index], last_position_index)


else:
    pass


# Closing down the robot - we still only want to execute this if the object
# robot_connected is True
if robot_connected:

    # This is now the end of the code
    # So we send the robot to the sleep_joints position
    robot.move_joints(*sleep_joints)

    # We set learning mode to true (this is what basically releases the torque in the motors)
    robot.set_learning_mode(True)

    # We disconnect from the robot
    robot.quit()

    # Although the robot has cone to sleep
    # We still need to return the linear rail
    # The following code should handle this
    travel_dist_global = 600
    Linear_Rail_Instructions.linear_rail_move(travel_dist_global, clockwise=False)

    # Now output the data as a pandas data frame so that it can be saved to csv
    df = pd.DataFrame(updated_test_data, columns=['x coordinate', 'y coordinate', 'Sensor Value'])

    # Create the root window and hide it
    root = tk.Tk()
    #root.withdraw()

    # Ask the user where to save
    csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    # If the user exits or cancels then cancel the operation
    if not csv_file:
        print("Save canceled. Exiting.")
        exit()

    # Save the CSV
    df.to_csv(csv_file, index=False)

else:
    pass

