#!/usr/bin/env python3
"""
Quick Motor Test Script for PCA9685
Tests a single motor/servo connected to the PCA9685
"""

import time
import sys
sys.path.append('src')
from servo_controller import ServoController

def test_single_motor():
    """Test a single motor on channel 0"""
    print("=" * 50)
    print("PCA9685 Motor/Servo Quick Test")
    print("=" * 50)
    print("\nInitializing servo controller...")
    
    try:
        # Initialize the servo controller
        controller = ServoController(channels=16)
        
        # Which channel is your motor connected to?
        channel = 0  # Change this if your motor is on a different channel
        
        print(f"\nTesting motor on channel {channel}")
        print("The motor will move through several positions...")
        
        # Test sequence - move through different angles
        test_positions = [
            (90, "Center position"),
            (0, "Minimum position (0°)"),
            (180, "Maximum position (180°)"),
            (90, "Back to center"),
            (45, "45°"),
            (135, "135°"),
            (90, "Final center position")
        ]
        
        for angle, description in test_positions:
            print(f"\nMoving to {angle}° - {description}")
            controller.move_servo(channel, angle)
            time.sleep(1.5)  # Wait to see the movement
        
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        print("=" * 50)
        print("\nIf the motor moved through the positions, your setup is working!")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("\nTroubleshooting:")
        print("1. Check that the PCA9685 is properly connected to I2C (SDA, SCL)")
        print("2. Verify the motor/servo is connected to channel 0 (or change 'channel' variable)")
        print("3. Make sure the PCA9685 is powered")
        print("4. Run 'sudo i2cdetect -y 1' to verify the PCA9685 is detected")

if __name__ == "__main__":
    print("\nMake sure:")
    print("  - PCA9685 is connected to I2C (SDA/SCL)")
    print("  - Motor/Servo is connected to channel 0 (or adjust script)")
    print("  - PCA9685 has power connected (V+, GND, VCC)")
    
    input("\nPress Enter to start the test (Ctrl+C to quit)...")
    test_single_motor()

