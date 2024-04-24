from smd.red import *
import math
import keyboard
import time

# Robot parameters 
d = 0.269 # Distance between wheels in meters (track width)
wheel_radius = 0.074 / 2 # Radius of the wheels in meters
rpm_left = 0 # Initial RPM for the left motor
rpm_right = 0 # Intial RPM for the right motor
increment_rpm = 10 # RPM increment value
increment_omega = 10 # Omega increment value

port = "/dev/ttyUSB0"
m = Master(port)
m.attach(0)
m.attach(1) 

print(m.scan_modules(0))
print(m.scan_modules(1))

m.set_operation_mode(0, 2)
m.set_operation_mode(1, 2)

def calculate_wheel_velocity(rpm, wheel_radius):
    """Calculate linear velocity based on RPM and wheel radius."""
    return (2 * math.pi * wheel_radius * rpm) / 60

def calculate_robot_velocity(rpm_left, rpm_right, wheel_radius, d):
    """Calculate the linear and angular velocities of the robot."""
    v_left = calculate_wheel_velocity(rpm_left, wheel_radius)
    v_right = calculate_wheel_velocity(rpm_right, wheel_radius)
    v = (v_left + v_right) / 2
    omega = (v_right - v_left) / d
    return v, omega

def print_velocities(rpm_left, rpm_right, wheel_radius, d):
    """Calculate and print the robot's velocities."""
    v, omega = calculate_robot_velocity(rpm_left, rpm_right, wheel_radius, d)
    m.set_velocity(0, rpm_left)
    m.set_velocity(1, rpm_right)
    print(f"RPM Left: {rpm_left:.3f}, RPM Right: {rpm_right:.3f}, Linear Velocity: {v:.3f} m/s, Angular Velocity: {omega:.2f} rad/s")


def main():

    # Main loop
    print("Use arrow keys to adjust RPMs and Omega. Press 'esc' to exit.")
    while True:
        time.sleep(0.1)  # Reduce CPU usage
        if keyboard.is_pressed('up'):
            rpm_left += increment_rpm
            rpm_right += increment_rpm
            print_velocities(rpm_left, rpm_right, wheel_radius, d)
            time.sleep(0.2)  # Debouncing
        elif keyboard.is_pressed('down'):
            rpm_left = max(0, rpm_left - increment_rpm)
            rpm_right = max(0, rpm_right - increment_rpm)
            print_velocities(rpm_left, rpm_right, wheel_radius, d)
            time.sleep(0.2)  # Debouncing
        elif keyboard.is_pressed('left'):
            rpm_left -= increment_omega
            rpm_right += increment_omega
            print_velocities(rpm_left, rpm_right, wheel_radius, d)
            time.sleep(0.2)  # Debouncing
        elif keyboard.is_pressed('right'):
            rpm_left += increment_omega
            rpm_right -= increment_omega
            print_velocities(rpm_left, rpm_right, wheel_radius, d)
            time.sleep(0.2)  # Debouncing
        elif keyboard.is_pressed('esc'):
            break

print("Program exited gracefully.")

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("End program")