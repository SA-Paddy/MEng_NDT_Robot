# We have chosen to control the linear rail motor through the I/O outputs provided on the NiryoOne Arm
# The driver being used is a DM556 stepper driver - driving a motor which has 200 steps per revolution
# Our linear rail moves 5/6 mm per revolution (this has to be further clarified)
# The driver will have its own external power supply and be connected to the stepper motor directly
# Control signaling is therefore through the I/O outputs on the NiryoOne arm
# Control is achieved through pulse width modulation
# There are three factors involved in the control Step Pulse, Direction Pulse and Enablement Pulse.
# Looking at the driver documentation the following becomes clear
# Driving pulse needs to be less than 5v at high and less than 0.5 v when low
# Pulses should have a pulse width not less than 2.5 micro seconds (low or high)
# Direction pulse must preceed drive pulse by no less than 5 micro seconds
# Enablement pulse must preceed direction pulse by no less than 5 microseconds

# First we import the libraries - not because we need them here - but incase we want to run this code independently of main
from niryo_one_tcp_client import *
import time
import math

# define what robot is
robot=NiryoOneClient()

# To simplify this code lets create a variable holder that our function calls on to figure out how many steps it needs to undertake
travel_dist_global = 1000
clockwise = True


# Now define one function to control our linear rail each time it is called with a value being passed from travel_dist
def linear_rail_move(travel_dist_global, clockwise=True):

    # Bring in the travel_dist_global variable and assign it to a new holder for us to use
    travel_dist = travel_dist_global

    if clockwise:
        dir_pin = 1
    else:
        dir_pin = 0

    print(dir_pin)

    # Lets develop constants to hold our constraints
    # This just makes it easier to change these variables if we need to
    steps_per_revolution = 200
    mm_per_revolution = 5
    min_pulse_width = 2.5e-6 # 2.5 microseconds
    min_pulse_delay = 5e-6 # 5 microseconds

    # Lets work out how many revolutions are required for the set amount of travel_dist
    revolutions = travel_dist / mm_per_revolution

    # Now we figure out how many pulses we need to step the motor
    drive_pulses = revolutions * steps_per_revolution

    # Now we enable the driver with a signal
    # We will be using GPIO_1A (enum 0) for drive, GPIO_1B (enum 1) for direction and GPIO_1C (enum 2) for enablement
    # First we set the pin states for all pins (0 is input, 1 is output - from enums)
    robot.set_pin_mode(0, 1)
    robot.set_pin_mode(1, 1)
    robot.set_pin_mode(2, 1)

    # Now we drive the enablement pulse (pin GPIO_1C enum 1) digital state low is 0 and high is 1
    robot.digital_write(1, 1)
    # Run this for a period of time (at least 5 microseconds) to ensure drive is enabled before next instruction
    time.sleep(min_pulse_delay)

    # Now we drive the directional pin GPIO_1B (enum 1) to clockwise (we think this is high)
    robot.digital_write(1, dir_pin)
    # Run the directional pulse for a minimum time before implementing the next instruction

    # Now we step the motor
    # Create a loop that will continuously run until the condition has been met
    for _ in range(int(drive_pulses)):
        # Drive Pulse On (GPIO_1A is enum 0, High is enum 1)
        robot.digital_write(0, 1)
        # Run the pulse for the minimum pulse width
        time.sleep(min_pulse_width)
        # Drive Pulse Off (GPIO_1A is enum 0, High is enum 1)
        robot.digital_write(0, 0)
        # Run for the minimum pulse width
        time.sleep(min_pulse_width)

    # Disable the stepper driver
    robot.digital_write(2, 0)

    return


# linear_rail_move(travel_dist_global, clockwise)

