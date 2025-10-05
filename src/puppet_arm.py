"""
Puppet Arm Controller
Manages arm movements with multiple servos per arm
"""

import time
from servo_controller import ServoController

class PuppetArm:
    def __init__(self, servo_controller, arm_config):
        """
        Initialize a puppet arm
        
        Args:
            servo_controller: ServoController instance
            arm_config: Dictionary with servo channel mappings
                Example: {
                    'shoulder': 0,      # Servo channel for shoulder
                    'elbow': 1,         # Servo channel for elbow  
                    'wrist': 2          # Servo channel for wrist (optional)
                }
        """
        self.servo_controller = servo_controller
        self.config = arm_config
        self.current_pose = {}
        
        # Initialize all servos to center position
        self.reset_to_center()
    
    def reset_to_center(self):
        """Reset all arm servos to center position"""
        for joint, channel in self.config.items():
            self.servo_controller.move_servo(channel, 90)
            self.current_pose[joint] = 90
        time.sleep(0.5)
    
    def move_to_pose(self, pose, speed=None):
        """
        Move arm to a specific pose
        
        Args:
            pose: Dictionary with joint angles
                Example: {'shoulder': 45, 'elbow': 120, 'wrist': 90}
            speed: Movement speed for smooth motion
        """
        print(f"Moving to pose: {pose}")
        
        for joint, angle in pose.items():
            if joint in self.config:
                channel = self.config[joint]
                self.servo_controller.move_servo(channel, angle, speed)
                self.current_pose[joint] = angle
            else:
                print(f"Warning: Joint '{joint}' not found in arm configuration")
        
        # Small delay to ensure movement completes
        time.sleep(0.5)
    
    def get_current_pose(self):
        """Get current pose of the arm"""
        return self.current_pose.copy()
    
    def wave_motion(self, cycles=3, speed=5):
        """
        Perform a waving motion
        
        Args:
            cycles: Number of wave cycles
            speed: Speed of the wave motion
        """
        print(f"Performing wave motion ({cycles} cycles)")
        
        # Store original position
        original_pose = self.get_current_pose()
        
        for _ in range(cycles):
            # Wave up
            wave_pose = {
                'shoulder': 45,
                'elbow': 90
            }
            if 'wrist' in self.config:
                wave_pose['wrist'] = 60
            
            self.move_to_pose(wave_pose, speed)
            time.sleep(0.3)
            
            # Wave down
            wave_pose = {
                'shoulder': 45,
                'elbow': 90
            }
            if 'wrist' in self.config:
                wave_pose['wrist'] = 120
            
            self.move_to_pose(wave_pose, speed)
            time.sleep(0.3)
        
        # Return to original position
        self.move_to_pose(original_pose, speed)
    
    def raise_arm(self, speed=None):
        """Raise the arm up"""
        pose = {
            'shoulder': 30,
            'elbow': 60
        }
        if 'wrist' in self.config:
            pose['wrist'] = 90
        
        self.move_to_pose(pose, speed)
    
    def lower_arm(self, speed=None):
        """Lower the arm down"""
        pose = {
            'shoulder': 150,
            'elbow': 120
        }
        if 'wrist' in self.config:
            pose['wrist'] = 90
        
        self.move_to_pose(pose, speed)


class PuppetController:
    def __init__(self):
        """Initialize the main puppet controller"""
        self.servo_controller = ServoController()
        self.arms = {}
        
        # Default arm configurations (you can modify these based on your wiring)
        self.arm_configs = {
            'left_arm': {
                'shoulder': 0,  # Left shoulder servo channel
                'elbow': 1,     # Left elbow servo channel
                'wrist': 2      # Left wrist servo channel (optional)
            },
            'right_arm': {
                'shoulder': 3,  # Right shoulder servo channel  
                'elbow': 4,     # Right elbow servo channel
                'wrist': 5      # Right wrist servo channel (optional)
            }
        }
        
        # Initialize arms
        for arm_name, config in self.arm_configs.items():
            self.arms[arm_name] = PuppetArm(self.servo_controller, config)
    
    def reset_all_arms(self):
        """Reset all arms to center position"""
        print("Resetting all arms to center position")
        for arm in self.arms.values():
            arm.reset_to_center()
    
    def get_arm(self, arm_name):
        """Get a specific arm controller"""
        return self.arms.get(arm_name)
    
    def both_arms_wave(self, cycles=3):
        """Make both arms wave simultaneously"""
        print("Both arms waving!")
        # You could implement this with threading for simultaneous movement
        # For now, we'll do them sequentially
        if 'left_arm' in self.arms and 'right_arm' in self.arms:
            self.arms['left_arm'].wave_motion(cycles)
            self.arms['right_arm'].wave_motion(cycles)
