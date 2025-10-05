#!/usr/bin/env python3
"""
Test All Motors Script
Helps you identify which motor is connected to which channel
and ensure all motors are working
"""

import time
import sys
sys.path.append('src')
from servo_controller import ServoController

def test_all_motors():
    """Test motors one at a time to identify which is which"""
    print("=" * 60)
    print("MULTI-MOTOR TEST - Identify Your Motor Channels")
    print("=" * 60)
    print("\nThis script will test each channel one at a time")
    print("so you can identify which motor is which.")
    print("\nHow many motors do you have connected?")
    
    try:
        num_motors = int(input("Enter number (2-6): "))
        if num_motors < 2 or num_motors > 16:
            print("Please enter a number between 2 and 16")
            return
    except ValueError:
        print("Invalid input")
        return
    
    print(f"\nOkay, testing {num_motors} motors...")
    print("Watch which motor moves and write down the channel number!\n")
    
    controller = ServoController(channels=16)
    
    # Dictionary to store motor assignments
    motor_map = {}
    
    for channel in range(num_motors):
        print("\n" + "=" * 60)
        print(f"Testing Channel {channel}")
        print("=" * 60)
        
        # Move this motor through a sequence
        print(f"\nChannel {channel} will now move...")
        print("Watch your puppet - which motor is moving?")
        
        # Distinctive movement pattern
        controller.move_servo(channel, 90)  # Center
        time.sleep(1)
        controller.move_servo(channel, 45)  # Left
        time.sleep(1)
        controller.move_servo(channel, 135) # Right
        time.sleep(1)
        controller.move_servo(channel, 0)  # Back to center
        time.sleep(1)
        
        # Ask user to identify
        label = input(f"\nWhich motor was that? (e.g., 'left_shoulder', 'right_elbow'): ").strip()
        if label:
            motor_map[label] = channel
            print(f"✓ Recorded: {label} = Channel {channel}")
        
        if channel < num_motors - 1:
            input("\nPress Enter to test next channel...")
    
    # Display the mapping
    print("\n" + "=" * 60)
    print("MOTOR MAPPING RESULTS")
    print("=" * 60)
    print("\nYour motor configuration:")
    for motor_name, channel_num in motor_map.items():
        print(f"  {motor_name}: Channel {channel_num}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("\n1. Open src/puppet_arm.py")
    print("2. Update the arm_configs dictionary with your channel numbers:")
    print("\n   self.arm_configs = {")
    print("       'left_arm': {")
    
    # Try to auto-generate the config
    left_motors = {k: v for k, v in motor_map.items() if 'left' in k.lower()}
    right_motors = {k: v for k, v in motor_map.items() if 'right' in k.lower()}
    
    if left_motors:
        for motor_name, channel in left_motors.items():
            joint = motor_name.replace('left_', '').replace('left', '')
            print(f"           '{joint}': {channel},")
    else:
        print("           'shoulder': ?,")
        print("           'elbow': ?,")
    
    print("       },")
    print("       'right_arm': {")
    
    if right_motors:
        for motor_name, channel in right_motors.items():
            joint = motor_name.replace('right_', '').replace('right', '')
            print(f"           '{joint}': {channel},")
    else:
        print("           'shoulder': ?,")
        print("           'elbow': ?,")
    
    print("       }")
    print("   }")
    
    print("\n3. Save the file")
    print("4. Run: python3 puppet_demo.py")
    
    # Test all motors together
    print("\n" + "=" * 60)
    input("\nPress Enter to test ALL motors together (move to center)...")
    print("Moving all motors to center position...")
    for channel in range(num_motors):
        controller.move_servo(channel, 90)
    print("✓ All motors centered!")

if __name__ == "__main__":
    print("\nMAKE SURE:")
    print("  ✓ All your motors are connected to the PCA9685")
    print("  ✓ PCA9685 has power connected")
    print("  ✓ You can see all your motors/servos")
    
    input("\nPress Enter to start testing (Ctrl+C to quit)...")
    try:
        test_all_motors()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

