#!/usr/bin/env python3
"""
Simple test script - moves first two motors back and forth
"""

import time
import sys
sys.path.append('src')
from servo_controller import ServoController

print("=" * 50)
print("Testing First Two Motors")
print("=" * 50)
print("\nThis will move motors on channels 0 and 1")
print("from 0° to 180° and back, 3 times each\n")

input("Press Enter to start...")

controller = ServoController(channels=16)

# Test channel 0
print("\n--- Testing Channel 0 ---")
for i in range(3):
    print(f"  Cycle {i+1}/3")
    print("    Moving to 0°")
    controller.move_servo(0, 0)
    time.sleep(1)
    print("    Moving to 180°")
    controller.move_servo(0, 180)
    time.sleep(1)

print("  Returning to center (90°)")
controller.move_servo(0, 90)
time.sleep(1)

# Test channel 1
print("\n--- Testing Channel 1 ---")
for i in range(3):
    print(f"  Cycle {i+1}/3")
    print("    Moving to 0°")
    controller.move_servo(1, 0)
    time.sleep(1)
    print("    Moving to 180°")
    controller.move_servo(1, 180)
    time.sleep(1)

print("  Returning to center (90°)")
controller.move_servo(1, 90)
time.sleep(1)

print("\n" + "=" * 50)
print("Test Complete!")
print("=" * 50)

