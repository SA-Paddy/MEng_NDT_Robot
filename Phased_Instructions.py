import time
import serial
from niryo_one_tcp_client import *

robot = NiryoOneClient()
sleep_joints = [0.0, 0.55, -1.2, 0.0, 0.0, 0.0]

# Create a list for the updated test data
updated_test_data = []

# We define a function that we can call which will undertake the first set of moves
# This function will need to import data from the local world
# The data it will need to call on is the coordinates tuple list and the sleep_joints object
def Phase_Move_One(coordinates, sleep_joints):
    # Rotate the robot by 90 degrees clockwise
    robot.move_joints([-1.57], sleep_joints[1], sleep_joints[2], sleep_joints[3], sleep_joints[4], sleep_joints[5])
    # Allow enough time for the movement to take effect
    time.sleep(1)

    # This code creates a for loop
    # Please see phase two for more detailed comments explaining how it works
    for index, (x, y) in enumerate(coordinates):
        # This just says that the loop should 'break' if y is found to be larger than 25
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

                # Because we altered the coordinate system earlier in this code
                # We now need to remove our alteration before saving to the
                # Test data holder
                corrected_coordinate = (x, y + 125)

                # Here we just append the data to the object called updated_test_data
                # The formatting ((variable/s)) defines this as a Tuple list
                # The benefit of using a Tuple list is that it is immutable
                # All this means is that once the data is created it cant be altered
                updated_test_data.append((corrected_coordinate, sensor_value))

                # We then update the last_position_index object with the current index value
                last_position_index = index

                # This just closes the function down but tells the function to return to local
                # World the updated_test_data information as well as the last_position_index
                return updated_test_data, last_position_index


# We define a function that we can call which will undertake the second set of moves
# This function will need to import data from the local world
# The data it will need to call on is the coordinates tuple list and the last_position_index object
def Phase_Move_Two(coordinates, last_position_index):
    # We need to start on the coordinate set one step past where we last left off
    start_index = last_position_index + 1

    # This code creates a 'for' loop - it essentially loops for every value of index
    # Pulling every tuple out of  the coordinates list
    # Until the break conditions are met (y>350)
    # (x, y) in enumerate(coordinates[start_index:].....
    # This part tells the code to unpack the tuple list found in coordinates object
    # Whilst it is unpacking it is telling it to number each tuple
    # [start_index:] defines the starting tuple to look at in the list
    # So as an example - it tells it to look at coordinates[2] meaning the third Tuple
    # (List positions start counting from the first element being 0)
    # The start=start_index): part tells it to number this element to whatever start_index is
    # The reason for this is to ensure that indexing remains consistent between all phases
    # Therefore reducing  the possibility for errors or issues
    for index, (x, y) in enumerate(coordinates[start_index:], start=start_index):
        # This just tells the loop to 'break' if y is larger than 350
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

                # Because we altered the coordinate system earlier in this code
                # We now need to remove our alteration before saving to the
                # Test data holder
                corrected_coordinate = (x, y + 450)

                # Here we just append the data to the object called updated_test_data
                # The formatting ((variable/s)) defines this as a Tuple list
                # The benefit of using a Tuple list is that it is immutable
                # All this means is that once the data is created it cant be altered
                updated_test_data.append((corrected_coordinate, sensor_value))

                # We then update the last_position_index object with the current index value
                last_position_index = index

                # This just closes the function down but tells the function to return to local
                # World the updated_test_data information as well as the last_position_index
                return updated_test_data, last_position_index

# We define a function that we can call which will undertake the Third set of moves
# This function will need to import data from the local world
# The data it will need to call on is the coordinates tuple list and the last_position_index object
def Phase_Move_Three(coordinates, last_position_index):

    # As before we create the starting index from the stored variable las_position_index
    # All we are doing is increasing its value by 1
    start_index = last_position_index + 1

    # Establish the for loop again - please refer to Phase_Move_Two for detailed
    # Comments explaining how this works
    for index, (x, y) in enumerate(coordinates[start_index:], start=start_index):
        # The code loops through until it meets the following criteria which causes it to break
        if y > 675:
            break

            # Whilst the loop is in progress - we move the robot accordingly
            robot.move_pose(x, y - 775, 0, 0, 0, 0)

            # We create a time delay to allow the movement to take place
            time.sleep(1)

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0:
                # Strip the data packet down to only a float
                datapacket = arduinoData.readline().decode('utf-8').strip('\r\n')
                # Store the data locally as a float
                sensor_value = float(datapacket)

                # Close the connection to the Arduino
                arduinoData.close()

                # Because we altered the coordinate system earlier in this code
                # We now need to remove our alteration before saving to the
                # Test data holder
                corrected_coordinate = (x, y + 775)

                # Here we just append the data to the object called updated_test_data
                # The formatting ((variable/s)) defines this as a Tuple list
                # The benefit of using a Tuple list is that it is immutable
                # All this means is that once the data is created it cant be altered
                updated_test_data.append((corrected_coordinate, sensor_value))

                # We then update the last_position_index object with the current index value
                last_position_index = index

                # This just closes the function down but tells the function to return to local
                # World the updated_test_data information as well as the last_position_index
                return updated_test_data, last_position_index

# We define a function that we can call which will undertake the Fourth set of moves
# This function will need to import data from the local world
# The data it will need to call on is the coordinates tuple list and the last_position_index object
def Phase_Move_Four(coordinates, last_position_index):

    # In the Fourth movement phase we are moving to the otherside of where we have been testing
    # This means that we need to rotate j1 anti-clockwise by 180 degrees or pi radians
    # To ensure we do so safely we must first ensure that the arm will not interact with anything in the environment
    # The simplest way to do this is to adopt the sleep position - which re-centres j1
    # Therefore we would only need to rotate by 90 degrees anti-clockwise from this pose
    # sleep_joints is already a classified object in the environment where we will be calling this function
    # So there is no need to define it within this function
    robot.move_joints(*sleep_joints)

    # Now that the arm is safely out of the way - we can rotate j1
    # once tis  rotation is complete - we can continue with the rest of the script
    robot.move_joints(1.57, sleep_joints[1], sleep_joints[2], sleep_joints[3], sleep_joints[4], sleep_joints[5])

    # Lets put in a time delay to enable the movement to take place
    time.sleep(1)

    # As before we create the starting index from the stored variable last_position_index
    # All we are doing is increasing its value by 1
    start_index = last_position_index + 1

    # Establish the for loop again - please refer to Phase_Move_Two for detailed
    # Comments explaining how this works
    for index, (x, y) in enumerate(coordinates[start_index:], start=start_index):
        # The code loops through until it meets the following criteria which causes it to break
        if y > 800:
            break

            # Whilst the loop is in progress - we move the robot accordingly
            robot.move_pose(x, y + 175, 0, 0, 0, 0)

            # We create a time delay to allow the movement to take place
            time.sleep(1)

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0:
                # Strip the data packet down to only a float
                datapacket = arduinoData.readline().decode('utf-8').strip('\r\n')
                # Store the data locally as a float
                sensor_value = float(datapacket)

                # Close the connection to the Arduino
                arduinoData.close()

                # Because we altered the coordinate system earlier in this code
                # We now need to remove our alteration before saving to the
                # Test data holder
                corrected_coordinate = (x, y - 175)

                # Here we just append the data to the object called updated_test_data
                # The formatting ((variable/s)) defines this as a Tuple list
                # The benefit of using a Tuple list is that it is immutable
                # All this means is that once the data is created it cant be altered
                updated_test_data.append((corrected_coordinate, sensor_value))

                # We then update the last_position_index object with the current index value
                last_position_index = index

                # This just closes the function down but tells the function to return to local
                # World the updated_test_data information as well as the last_position_index
                return updated_test_data, last_position_index

# We define a function that we can call which will undertake the Fifth set of moves
# This function will need to import data from the local world
# The data it will need to call on is the coordinates tuple list and the last_position_index object
def Phase_Move_Five(coordinates, last_position_index):

    # As before we create the starting index from the stored variable last_position_index
    # All we are doing is increasing its value by 1
    start_index = last_position_index + 1

    # Establish the for loop again - please refer to Phase_Move_Two for detailed
    # Comments explaining how this works
    for index, (x, y) in enumerate(coordinates[start_index:], start=start_index):
        # The code loops through until it meets the following criteria which causes it to break
        if y > 1000:
            break

            # Whilst the loop is in progress - we move the robot accordingly
            robot.move_pose(x, y + 400, 0, 0, 0, 0)

            # We create a time delay to allow the movement to take place
            time.sleep(1)

            # Check to see if there is data available
            if arduinoData.inWaiting() > 0:
                # Strip the data packet down to only a float
                datapacket = arduinoData.readline().decode('utf-8').strip('\r\n')
                # Store the data locally as a float
                sensor_value = float(datapacket)

                # Close the connection to the Arduino
                arduinoData.close()

                # Because we altered the coordinate system earlier in this code
                # We now need to remove our alteration before saving to the
                # Test data holder
                corrected_coordinate = (x, y - 400)

                # Here we just append the data to the object called updated_test_data
                # The formatting ((variable/s)) defines this as a Tuple list
                # The benefit of using a Tuple list is that it is immutable
                # All this means is that once the data is created it cant be altered
                updated_test_data.append((corrected_coordinate, sensor_value))

                # We then update the last_position_index object with the current index value
                last_position_index = index

                # This just closes the function down but tells the function to return to local
                # World the updated_test_data information as well as the last_position_index
                return updated_test_data, last_position_index