# Minecraft Parkour Generator 🎮

A dynamic Minecraft mod implemented in Python that generates exciting parkour courses across 10 difficulty levels, ranging from beginner to expert. Challenge yourself with progressively harder parkour stages featuring various obstacles, special effects, and unique challenges!

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![MCPI](https://img.shields.io/badge/MCPI-Compatible-orange.svg)

## 🌟 Features

- **10 Difficulty Levels**: Progress from beginner-friendly courses to expert challenges
- **Dynamic Generation**: Each parkour course is uniquely generated
- **Special Effects**: 
  - Water effects
  - Lighting effects
  - Particle systems
  - Visual feedback
- **Various Obstacles**:
  - Standard jumps
  - Ladder parkour
  - Thin bridges
  - Strategic platforms
- **Real-time Feedback**:
  - Fall counter
  - Achievement messages
  - Level progression
  - Colorful chat notifications

## 🎯 Prerequisites

- Python 3.6 or higher
- Minecraft Pi Edition or compatible server
- MCPI Python library
- Java 21

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeProTech/MinecraftParkourGen.git
```

2. Navigate to the project directory:
```bash
cd MinecraftParkourGen
```

3. Install required dependencies:
```bash
pip install mcpi
```

## 💻 Usage

1. Start Minecraft Pi Edition or your compatible Minecraft server

2. Run the generator:
```bash
python main.py
```

3. In Minecraft chat:
   - Type a number between 1-10 to select your difficulty level
   - Level 1 is beginner-friendly
   - Level 10 is expert difficulty

## 🎮 Gameplay

- **Starting Out**:
  - The game generates a spawn platform
  - Select your difficulty level via chat
  - Follow the parkour course to reach the goal

- **Difficulty Progression**:
  - Level 1-3: Basic jumps and simple platforms
  - Level 4-6: Introduces ladder parkour and longer jumps
  - Level 7-8: Adds thin bridges and complex combinations
  - Level 9-10: Expert level with maximum challenge

- **Features per Level**:
  - Increasing gap distances
  - More complex obstacle patterns
  - Strategic platform placement
  - Various special effects

## 🛠️ Technical Details

- Built with Python and MCPI library
- Modular code structure
- Dynamic obstacle generation
- Configurable difficulty settings
- Real-time player position tracking
- Efficient area clearing and regeneration

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎨 Credits

Created by [Stefanos](https://github.com/CodeProTech)
