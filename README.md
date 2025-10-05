# 🎭 Motorized String Puppet

A Raspberry Pi-controlled motorized string puppet system using PCA9685 PWM controller and servo motors.

## 🚀 Quick Start

### Hardware Setup
- Raspberry Pi (any model with GPIO)
- PCA9685 16-channel PWM controller
- Servo motors (4-6 for arms)
- External power supply for servos
- Jumper wires

### Software Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/zhazaz/puppetgit.git
   cd puppetgit
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure servo channels:**
   Edit `src/puppet_arm.py` and update the `arm_configs` dictionary to match your wiring:
   ```python
   self.arm_configs = {
       'left_arm': {
           'shoulder': 0,  # Your servo channel numbers
           'elbow': 1,
           'wrist': 2
       },
       'right_arm': {
           'shoulder': 3,
           'elbow': 4, 
           'wrist': 5
       }
   }
   ```

## 🎬 Usage

### Run Interactive Mode
```bash
python3 puppet_demo.py --interactive
```

### Run Demo Sequences
```bash
python3 puppet_demo.py --demo
```

### Execute Specific Pose
```bash
python3 puppet_demo.py --pose celebration
```

### Execute Specific Sequence
```bash
python3 puppet_demo.py --sequence greeting
```

### List Available Options
```bash
python3 puppet_demo.py --list poses
python3 puppet_demo.py --list sequences
```

## 📁 Project Structure

```
puppetgit/
├── puppet_demo.py          # Main demo script
├── requirements.txt        # Python dependencies
├── src/
│   ├── servo_controller.py # Low-level servo control
│   ├── puppet_arm.py       # Arm movement classes
│   └── sequence_controller.py # Sequence management
├── poses/
│   └── basic_poses.json    # Predefined poses
└── sequences/
    └── movement_sequences.json # Movement sequences
```

## 🎭 Available Poses

- **rest** - Neutral position
- **arms_raised** - Both arms up
- **arms_out** - Arms stretched to sides
- **celebration** - Victory pose
- **thinking** - Contemplative pose
- **pointing_left/right** - Pointing gestures
- **arms_crossed** - Arms crossed in front

## 🎬 Available Sequences

- **greeting** - Friendly wave sequence
- **celebration_dance** - Victory celebration
- **pointing_demo** - Left and right pointing
- **thinking_sequence** - Thoughtful movements
- **exercise_routine** - Arm exercises

## 🔧 Customization

### Adding New Poses
Edit `poses/basic_poses.json` to add custom poses:
```json
{
  "poses": {
    "my_custom_pose": {
      "description": "My custom pose",
      "left_arm": {
        "shoulder": 45,
        "elbow": 90,
        "wrist": 120
      },
      "right_arm": {
        "shoulder": 135,
        "elbow": 90,
        "wrist": 60
      }
    }
  }
}
```

### Creating Movement Sequences
Edit `sequences/movement_sequences.json` to create custom sequences:
```json
{
  "sequences": {
    "my_sequence": {
      "description": "My custom sequence",
      "steps": [
        {
          "pose": "rest",
          "duration": 1.0,
          "speed": 3
        },
        {
          "pose": "my_custom_pose", 
          "duration": 2.0,
          "speed": 4
        }
      ]
    }
  }
}
```

## 🔌 Hardware Connections

### PCA9685 to Raspberry Pi
- VCC → 3.3V or 5V
- GND → GND  
- SCL → GPIO 3 (SCL)
- SDA → GPIO 2 (SDA)

### Servos to PCA9685
- Connect servo signal wires to PWM channels 0-15
- Connect servo power and ground to external power supply through PCA9685

## 🎯 Next Steps

- Add more complex sequences
- Implement web interface for remote control
- Add sensor integration for interactive responses
- Expand to control legs and head movements
- Add voice commands

## 🤝 Contributing

Feel free to add new poses, sequences, or features! This is a learning project for Raspberry Pi servo control.

## 📝 License

This project is open source - feel free to modify and share!
