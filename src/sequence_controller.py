"""
Sequence Controller for Puppet Movements
Loads and executes predefined movement sequences
"""

import json
import time
import os
from puppet_arm import PuppetController

class SequenceController:
    def __init__(self, puppet_controller):
        """
        Initialize sequence controller
        
        Args:
            puppet_controller: PuppetController instance
        """
        self.puppet = puppet_controller
        self.poses = {}
        self.sequences = {}
        
        # Load poses and sequences
        self.load_poses()
        self.load_sequences()
    
    def load_poses(self, poses_file="poses/basic_poses.json"):
        """Load poses from JSON file"""
        try:
            with open(poses_file, 'r') as f:
                data = json.load(f)
                self.poses = data.get('poses', {})
            print(f"Loaded {len(self.poses)} poses")
        except FileNotFoundError:
            print(f"Poses file {poses_file} not found")
        except json.JSONDecodeError:
            print(f"Error reading poses file {poses_file}")
    
    def load_sequences(self, sequences_file="sequences/movement_sequences.json"):
        """Load sequences from JSON file"""
        try:
            with open(sequences_file, 'r') as f:
                data = json.load(f)
                self.sequences = data.get('sequences', {})
            print(f"Loaded {len(self.sequences)} sequences")
        except FileNotFoundError:
            print(f"Sequences file {sequences_file} not found")
        except json.JSONDecodeError:
            print(f"Error reading sequences file {sequences_file}")
    
    def execute_pose(self, pose_name, speed=None):
        """
        Execute a single pose
        
        Args:
            pose_name: Name of the pose to execute
            speed: Movement speed (optional)
        """
        if pose_name not in self.poses:
            print(f"Pose '{pose_name}' not found")
            return False
        
        pose_data = self.poses[pose_name]
        print(f"Executing pose: {pose_name} - {pose_data.get('description', '')}")
        
        # Move each arm to its pose
        for arm_name, arm_pose in pose_data.items():
            if arm_name == 'description':
                continue
                
            arm = self.puppet.get_arm(arm_name)
            if arm:
                arm.move_to_pose(arm_pose, speed)
            else:
                print(f"Warning: Arm '{arm_name}' not found")
        
        return True
    
    def execute_sequence(self, sequence_name):
        """
        Execute a complete movement sequence
        
        Args:
            sequence_name: Name of the sequence to execute
        """
        if sequence_name not in self.sequences:
            print(f"Sequence '{sequence_name}' not found")
            return False
        
        sequence_data = self.sequences[sequence_name]
        print(f"\\nExecuting sequence: {sequence_name}")
        print(f"Description: {sequence_data.get('description', 'No description')}")
        print(f"Steps: {len(sequence_data.get('steps', []))}")
        
        steps = sequence_data.get('steps', [])
        
        for i, step in enumerate(steps):
            print(f"\\nStep {i+1}/{len(steps)}: {step.get('pose', 'unknown')}")
            
            pose_name = step.get('pose')
            speed = step.get('speed')
            duration = step.get('duration', 1.0)
            
            # Execute the pose
            if self.execute_pose(pose_name, speed):
                # Wait for the specified duration
                time.sleep(duration)
            else:
                print(f"Failed to execute pose: {pose_name}")
        
        print(f"\\nSequence '{sequence_name}' completed!")
        return True
    
    def list_poses(self):
        """List all available poses"""
        print("\\nAvailable poses:")
        for pose_name, pose_data in self.poses.items():
            description = pose_data.get('description', 'No description')
            print(f"  - {pose_name}: {description}")
    
    def list_sequences(self):
        """List all available sequences"""
        print("\\nAvailable sequences:")
        for seq_name, seq_data in self.sequences.items():
            description = seq_data.get('description', 'No description')
            steps = len(seq_data.get('steps', []))
            print(f"  - {seq_name}: {description} ({steps} steps)")
    
    def create_custom_pose(self, pose_name, left_arm_angles, right_arm_angles, description="Custom pose"):
        """
        Create a custom pose on the fly
        
        Args:
            pose_name: Name for the new pose
            left_arm_angles: Dict with left arm joint angles
            right_arm_angles: Dict with right arm joint angles
            description: Description of the pose
        """
        new_pose = {
            'description': description,
            'left_arm': left_arm_angles,
            'right_arm': right_arm_angles
        }
        
        self.poses[pose_name] = new_pose
        print(f"Created custom pose: {pose_name}")
    
    def demo_all_poses(self, delay=2.0):
        """
        Demonstrate all available poses
        
        Args:
            delay: Delay between poses in seconds
        """
        print("\\nDemonstrating all poses...")
        for pose_name in self.poses.keys():
            self.execute_pose(pose_name)
            time.sleep(delay)
        
        # Return to rest position
        self.execute_pose('rest')
    
    def interactive_mode(self):
        """
        Interactive mode for testing poses and sequences
        """
        print("\\n=== Puppet Interactive Mode ===")
        print("Commands:")
        print("  pose <name>     - Execute a pose")
        print("  seq <name>      - Execute a sequence") 
        print("  list poses      - List all poses")
        print("  list sequences  - List all sequences")
        print("  demo poses      - Demo all poses")
        print("  reset           - Reset to center position")
        print("  quit            - Exit interactive mode")
        
        while True:
            try:
                command = input("\\n> ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'list poses':
                    self.list_poses()
                elif command == 'list sequences':
                    self.list_sequences()
                elif command == 'demo poses':
                    self.demo_all_poses()
                elif command == 'reset':
                    self.puppet.reset_all_arms()
                elif command.startswith('pose '):
                    pose_name = command[5:].strip()
                    self.execute_pose(pose_name)
                elif command.startswith('seq '):
                    seq_name = command[4:].strip()
                    self.execute_sequence(seq_name)
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\\nExiting interactive mode...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Reset puppet before exiting
        self.puppet.reset_all_arms()
