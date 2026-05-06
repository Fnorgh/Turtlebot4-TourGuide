# ROS2 Gesture-Controlled Navigation

Gesture-based navigation using a TurtleBot 4 with person-follow and landmark touring.

## Project Overview

This system operates in **two phases**:

1. **Mapping Phase**  
   Build a SLAM map and save the home/landmark position.

2. **Autonomous Tour Phase**  
   Follow a person → stop → gesture → navigate → QR → speak → repeat.

## Full Manual Instructions

For a complete, unsimplified, step-by-step manual workflow, click [here](./manual_guide.md).

This includes:

- Full terminal-by-terminal setup
- Manual SLAM + Nav2 launching
- Gesture debugging
- QR + audio nodes
- Advanced troubleshooting

Use this guide for full control (outside of Shell scripts), debugging, and advanced testing.

---

# Setup

## First-Time Setup (run once per machine)

### 1. Build the package

```bash
cd ~/robotics/ros2-topological-mapping-navigation/ros2_ws
colcon build --packages-select topological_nav
```

## Python Environment (REQUIRED)

Used by gesture + person-follow nodes.

```bash
cd ~/robotics/ros2-topological-mapping-navigation/ros2_ws
pip install --user --break-system-packages virtualenv
~/.local/bin/virtualenv --system-site-packages venv

venv/bin/pip install -r requirements.txt
venv/bin/pip install ultralytics
venv/bin/pip install "numpy<2"

touch venv/COLCON_IGNORE
```

## Set Up Robot

First, SSH into the robot:

```bash
ssh student@<nameFromRobot>.cs.nor.ou.edu
```

Each robot has unique ROS settings. In a new terminal, run:

```bash
printf "<robot_name>" | robot-setup.sh
```

Copy the output values into the variables at the top of each `.sh` scripts

- `ROBOT_NAME`
- `ROS_DOMAIN_ID`
- `ROS_DISCOVERY_SERVER`

### Example

```bash
printf "leatherback" | robot-setup.sh
```

Use the output values in all terminals.

Valid robot names: `snapper`, `loggerhead`, `testudo`, `galapagos`, `terrapin`, `leatherback`, `hawksbill`, `matamata`, `softshell`

## Before Starting

Edit scripts with the previously obtained ROS settings:

```bash
ROBOT_NAME="your_robot"
ROS_DOMAIN_ID="your_id"
ROS_DISCOVERY_SERVER="your_server"
```

Make executable:

```bash
chmod +x start_mapping.sh
chmod +x start_landmarks.sh
chmod +x start_person_follow.sh
```

---

# Running the System (Shell Scripts)

## Phase 1 — Mapping

```bash
./start_mapping.sh
```

### What opens

- SLAM (map building)
- RViz (visualization)
- Teleop (keyboard control)
- Landmark Saver (for saving home/map)

### Instructions

- To set up visual mapping on Rviz, click [here](./manual_guide.md#rviz-setup).
- To set up a camera feed, click [here](./manual_guide.md#terminal-3-camera).

In the teleop terminal, drive the robot using:

| Keyboard Command | Movement      |
| :--------------: | :------------ |
|       `i`        | Move forward  |
|       `,`        | Move backward |
|       `j`        | Turn left     |
|       `;`        | Turn right    |
|       `k`        | Stop          |

Return to start position.

In the landmark terminal, add landmarks using:

| Keyboard Command | Action                    |
| :--------------: | :------------------------ |
|       `1`        | Set landmark 1            |
|       `2`        | Set landmark 2            |
|       `3`        | Set landmark 3            |
|       `h`        | Set home                  |
|       `s`        | Save to `landmarks.yaml`  |
|       `q`        | Save home directory files |

This creates:

- `~/map.yaml`
- `~/map.pgm`
- `~/robotics/ros2-topological-mapping-navigation/landmarks.yaml`

---

## Phase 2 — Run System

```bash
./start_person_follow.sh
```

Wait ~3.5 minutes for startup:

1. ~25s → initial pose and setup is complete
2. ~60s → Nav2 starts
3. ~120s → system is fully ready

Navigation will NOT work until this completes.

Audio feedback will play on the connected computer (not the robot). A terminal will also output the robot's exact speech.

### Instructions

- To set up visual mapping on Rviz, click [here](./manual_guide.md#rviz-setup).
- To set up a camera feed, click [here](./manual_guide.md#terminal-3-camera).

Robot will follow a person, stop when close, then wait for a gesture.

Show the following fingers to the camera:

| Gesture | Action     |
| :-----: | :--------- |
|    1    | Landmark 1 |
|    2    | Landmark 2 |
|    3    | Landmark 3 |
|    4    | Home       |

At each landmark, the robot will scan a QR code and speak the associated description.

- QR codes should contain: `task1`, `task2`, or `task3`.

If nothing happens, verify gestures with:

```bash
ros2 topic echo /gesture
```

---

# Notes

- Uses YOLOv8n for person detection
- Uses Mediapipe for gestures
- Uses Nav2 for navigation
- Landmarks saved in YAML
- Robot rotates ~180° after scanning a QR code to face the user again

---

# Team

University robotics project — TurtleBot 4 gesture-controlled navigation system.
