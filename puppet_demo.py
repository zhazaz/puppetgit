#!/usr/bin/env python3
"""
Main Puppet Demo Script
Demonstrates the capabilities of the motorized string puppet

Usage:
    python3 puppet_demo.py [options]

Options:
    --interactive    Start in interactive mode
    --demo          Run demo sequences
    --sequence <name>  Run specific sequence
    --pose <name>     Execute specific pose
"""

import sys
import os
import argparse
import time

# Add src directory to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from puppet_arm import PuppetController
from sequence_controller import SequenceController

def main():
    parser = argparse.ArgumentParser(description='Motorized String Puppet Controller')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    parser.add_argument('--demo', action='store_true', help='Run demo sequences')
    parser.add_argument('--sequence', type=str, help='Run specific sequence')
    parser.add_argument('--pose', type=str, help='Execute specific pose')
    parser.add_argument('--list', choices=['poses', 'sequences'], help='List available poses or sequences')
    
    args = parser.parse_args()
    
    print("🎭 Motorized String Puppet Controller")
    print("====================================")
    
    try:
        # Initialize the puppet controller
        print("Initializing puppet controller...")
        puppet = PuppetController()
        
        # Initialize sequence controller
        print("Loading poses and sequences...")
        sequencer = SequenceController(puppet)
        
        print("✅ Puppet ready!")
        print(f"📍 Servo channels configured:")
        for arm_name, config in puppet.arm_configs.items():
            print(f"   {arm_name}: {config}")
        
        # Reset puppet to center position
        print("\\n🔄 Resetting puppet to center position...")
        puppet.reset_all_arms()
        time.sleep(1)
        
        # Handle different modes
        if args.list:
            if args.list == 'poses':
                sequencer.list_poses()
            elif args.list == 'sequences':
                sequencer.list_sequences()
        
        elif args.pose:
            print(f"\\n🎭 Executing pose: {args.pose}")
            sequencer.execute_pose(args.pose)
        
        elif args.sequence:
            print(f"\\n🎬 Running sequence: {args.sequence}")
            sequencer.execute_sequence(args.sequence)
        
        elif args.demo:
            run_demo_sequences(sequencer)
        
        elif args.interactive:
            sequencer.interactive_mode()
        
        else:
            # Default behavior - show help and run a quick demo
            print("\\n" + "="*50)
            print("No specific command given. Here's what you can do:")
            print("\\n📋 Available commands:")
            print("  python3 puppet_demo.py --interactive")
            print("  python3 puppet_demo.py --demo")
            print("  python3 puppet_demo.py --list poses")
            print("  python3 puppet_demo.py --list sequences")
            print("  python3 puppet_demo.py --pose rest")
            print("  python3 puppet_demo.py --sequence greeting")
            
            print("\\n🎭 Quick demonstration:")
            # Quick demo
            time.sleep(2)
            sequencer.execute_pose('arms_raised')
            time.sleep(2)
            sequencer.execute_pose('rest')
            
    except KeyboardInterrupt:
        print("\\n\\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        print("Make sure your PCA9685 is connected and powered on!")
    finally:
        print("\\n🔄 Resetting puppet to safe position...")
        try:
            puppet.reset_all_arms()
        except:
            pass
        print("👋 Goodbye!")

def run_demo_sequences(sequencer):
    """Run a series of demo sequences"""
    print("\\n🎬 Running Demo Sequences")
    print("="*30)
    
    demo_sequences = [
        'greeting',
        'pointing_demo', 
        'celebration_dance',
        'thinking_sequence',
        'exercise_routine'
    ]
    
    for i, seq_name in enumerate(demo_sequences):
        print(f"\\n📽️  Demo {i+1}/{len(demo_sequences)}: {seq_name}")
        sequencer.execute_sequence(seq_name)
        
        if i < len(demo_sequences) - 1:  # Don't wait after last sequence
            print("⏳ Waiting 3 seconds before next sequence...")
            time.sleep(3)
    
    print("\\n🎉 Demo completed!")

if __name__ == "__main__":
    main()
