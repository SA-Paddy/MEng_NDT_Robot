import time
import serial
from niryo_one_tcp_client import *

robot = NiryoOneClient()

# Create a list for the updated test data
updated_test_data = []


def Phase_Mov_One(coordinates, sleep_joints):
    # Rotate the robot by 90 degrees clockwise
    robot.move_joints([-1.57], sleep_joints[1], sleep_joints[2], sleep_joints[3], sleep_joints[4], sleep_joints[5])
    # Allow enough time for the movement to take effect
    time.sleep(1)

    for index, (x, y) in enumerate(coordinates):
        if y > 25:
            break

            # We move the robot to the first pose
            robot.move_pose(x, y - 125, 0, 0, 0, 0)

            # We read the value from the arduino
            # First establish the serial connection
            arduinoData = serial.Serial('com10', 115200)
            # Allow time for the connection to stabilise
            time.sleep(1)

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0:
                # Strip the data packet down to only a float
                datapacket = arduinoData.readline().decode('utf-8').strip('\r\n')
                # Store the data locally as a float
                sensor_value = float(datapacket)

                # Close the connection to the Arduino
                arduinoData.close()

                corrected_coordinate = (x, y + 125)
                updated_test_data.append((corrected_coordinate, sensor_value))

                last_position_index = index

                return updated_test_data, last_position_index


def Phase_Mov_Two(coordinates, last_position_index):
    # We need to start on the coordinate set one step past where we last left off
    start_index = last_position_index + 1

    for index, (x, y) in enumerate(coordinates[start_index:], start=start_index):
        if y > 350:
            break

            # Move the robot through the poses as we go through this loop
            robot.move_pose(x, y - 450, 0, 0, 0, 0)
            # Pause to allow time to move
            time.sleep(1)

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0:
                # Strip the data packet down to only a float
                datapacket = arduinoData.readline().decode('utf-8').strip('\r\n')
                # Store the data locally as a float
                sensor_value = float(datapacket)

                # Close the connection to the Arduino
                arduinoData.close()

                corrected_coordinate = (x, y + 450)
                updated_test_data.append((corrected_coordinate, sensor_value))

                last_position_index = index

                return updated_test_data, last_position_index
