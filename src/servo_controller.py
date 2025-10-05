"""
Servo Controller for PCA9685 PWM Controller
Handles individual servo movements and calibration
"""

import time
import json
from adafruit_servokit import ServoKit

class ServoController:
    def __init__(self, channels=16, min_pulse=500, max_pulse=2500):
        """
        Initialize the PCA9685 servo controller
        
        Args:
            channels: Number of servo channels (default 16 for PCA9685)
            min_pulse: Minimum pulse width in microseconds
            max_pulse: Maximum pulse width in microseconds
        """
        self.kit = ServoKit(channels=channels)
        self.channels = channels
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        
        # Set pulse width ranges for all servos
        for i in range(channels):
            self.kit.servo[i].set_pulse_width_range(min_pulse, max_pulse)
    
    def move_servo(self, channel, angle, speed=None):
        """
        Move a servo to a specific angle
        
        Args:
            channel: Servo channel (0-15)
            angle: Target angle (0-180 degrees)
            speed: Movement speed (if None, moves immediately)
        """
        if 0 <= channel < self.channels and 0 <= angle <= 180:
            if speed is None:
                self.kit.servo[channel].angle = angle
            else:
                self._smooth_move(channel, angle, speed)
        else:
            print(f"Invalid channel ({channel}) or angle ({angle})")
    
    def _smooth_move(self, channel, target_angle, speed):
        """
        Move servo smoothly to target angle
        
        Args:
            channel: Servo channel
            target_angle: Target angle
            speed: Movement speed (degrees per step)
        """
        current_angle = self.kit.servo[channel].angle or 90  # Default to 90 if None
        
        if current_angle < target_angle:
            step = speed
        else:
            step = -speed
        
        angle = current_angle
        while abs(angle - target_angle) > abs(step):
            angle += step
            self.kit.servo[channel].angle = angle
            time.sleep(0.05)  # Small delay for smooth movement
        
        # Final position
        self.kit.servo[channel].angle = target_angle
    
    def get_servo_angle(self, channel):
        """Get current angle of a servo"""
        if 0 <= channel < self.channels:
            return self.kit.servo[channel].angle
        return None
    
    def set_all_servos_to_center(self):
        """Set all servos to center position (90 degrees)"""
        for i in range(self.channels):
            self.kit.servo[i].angle = 90
            time.sleep(0.1)  # Small delay between servos
    
    def disable_servo(self, channel):
        """Disable a servo (stop sending PWM signal)"""
        if 0 <= channel < self.channels:
            self.kit.servo[channel].angle = None
