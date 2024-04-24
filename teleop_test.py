from smd.red import *
import math
import keyboard
import time


class Robot:

    def __init__(self):
        # SMD setup
        self.port = "/dev/ttyUSB0"
        self.m = Master(self.port)
        self.m.attach(0)
        self.m.attach(1)
        print(self.m.scan_modules(Red(0)))
        print(self.m.scan_modules(Red(1)))

        self.m.set_operation_mode(0, 2)
        self.m.set_operation_mode(1, 2)

        # Robot parameters 
        self.d = 0.269 # Distance between wheels in meters (track width)
        self.wheel_radius = 0.074 / 2 # Radius of the wheels in meters
        self.rpm_left = 0 # Initial RPM for the left motor
        self.rpm_right = 0 # Intial RPM for the right motor
        self.increment_rpm = 10 # RPM increment value
        self.increment_omega = 10 # Omega increment value


    def calculate_wheel_velocity(self, rpm, wheel_radius):
        """Calculate linear velocity based on RPM and wheel radius."""
        return (2 * math.pi * wheel_radius * rpm) / 60

    def calculate_robot_velocity(self, rpm_left, rpm_right, wheel_radius, d):
        """Calculate the linear and angular velocities of the robot."""
        v_left = self.calculate_wheel_velocity(rpm_left, wheel_radius)
        v_right = self.calculate_wheel_velocity(rpm_right, wheel_radius)
        v = (v_left + v_right) / 2
        omega = (v_right - v_left) / d
        return v, omega

    def print_velocities(self, rpm_left, rpm_right, wheel_radius, d):
        """Calculate and print the robot's velocities."""
        v, omega = self.calculate_robot_velocity(rpm_left, rpm_right, wheel_radius, d)
        self.m.set_velocity(0, rpm_left)
        self.m.set_velocity(1, rpm_right)
        print(f"RPM Left: {rpm_left:.3f}, RPM Right: {rpm_right:.3f}, Linear Velocity: {v:.3f} m/s, Angular Velocity: {omega:.2f} rad/s")


    def main(self):

        # Main loop
        print("Use arrow keys to adjust RPMs and Omega. Press 'esc' to exit.")
        while True:
            time.sleep(0.1)  # Reduce CPU usage
            if keyboard.is_pressed('up'):
                rpm_left += self.increment_rpm
                rpm_right += self.increment_rpm
                self.print_velocities(rpm_left, rpm_right, self.wheel_radius, d)
                time.sleep(0.2)  # Debouncing
            elif keyboard.is_pressed('down'):
                rpm_left = max(0, self.rpm_left - self.increment_rpm)
                rpm_right = max(0, self.rpm_right - self.increment_rpm)
                self.print_velocities(rpm_left, rpm_right, self.wheel_radius, d)
                time.sleep(0.2)  # Debouncing
            elif keyboard.is_pressed('left'):
                rpm_left -= self.increment_omega
                rpm_right += self.increment_omega
                self.print_velocities(rpm_left, rpm_right, self.wheel_radius, d)
                time.sleep(0.2)  # Debouncing
            elif keyboard.is_pressed('right'):
                rpm_left += self.increment_omega
                rpm_right -= self.increment_omega
                self.print_velocities(rpm_left, rpm_right, self.wheel_radius, d)
                time.sleep(0.2)  # Debouncing
            elif keyboard.is_pressed('esc'):
                break


if __name__ == "__main__":

    try:
        t = Robot()
        t.main()

    except KeyboardInterrupt:
        print("End program")
