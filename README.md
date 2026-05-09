<img width="610" height="587" alt="nicklayingdown1" src="https://github.com/user-attachments/assets/acbf6701-caab-4ca0-b840-ec71fb1e0c76" />
<img width="3456" height="2304" alt="robotics" src="https://github.com/user-attachments/assets/c2ec3130-6986-4614-9e79-cee726147861" />
<div align="center">

# TurtleBot4 Tour Guide

### Gesture-Controlled Landmark Navigation with ROS 2

---

*Nicholas Louque · Noah Gibson · Jace Rausch — University of Oklahoma*

<br/>

![ROS2](https://img.shields.io/badge/ROS2_Humble-700000?style=flat-square&logo=ros&logoColor=FDF9D8)
![Python](https://img.shields.io/badge/Python_3.10+-700000?style=flat-square&logo=python&logoColor=FDF9D8)
![Mediapipe](https://img.shields.io/badge/Mediapipe-700000?style=flat-square&logoColor=FDF9D8)
![Nav2](https://img.shields.io/badge/Nav2-700000?style=flat-square&logoColor=FDF9D8)
![YOLOv8](https://img.shields.io/badge/YOLOv8-700000?style=flat-square&logoColor=FDF9D8)
![SLAM](https://img.shields.io/badge/SLAM_Toolbox-700000?style=flat-square&logoColor=FDF9D8)

<br/>

[![Read the Docs](https://img.shields.io/badge/Read_the_Docs-700000?style=for-the-badge&logoColor=FDF9D8)](https://github.com/Fnorgh/Turtlebot4-TourGuide/blob/main/manual_guide.md)
[![Project Poster](https://img.shields.io/badge/Project_Poster-700000?style=for-the-badge&logoColor=FDF9D8)](https://github.com/user-attachments/files/27560242/robotics.pdf)

</div>

---

## Demo

<table>
<tr>
<td width="50%" align="center" valign="top">

**Full System — Navigation Demo**

https://github.com/user-attachments/assets/7da67601-9a57-4d6e-9455-9c5c023634b7

*Gesture input through full autonomous navigation, QR scanning, and speech output*

</td>
<td width="50%" align="center" valign="top">

**SLAM Mapping and Localization**

https://github.com/user-attachments/assets/22ac0e2a-f9b1-444d-b467-b6c9ec6cb7c2

*LiDAR-based SLAM map building and Nav2 localization in the target environment*

</td>
</tr>
</table>

---

## Abstract

<table>
<tr>
<td width="60%" valign="top">

This project presents a **multimodal navigation system** for a TurtleBot 4 that allows users to guide a robot through hand gestures. The system combines **gesture recognition**, **QR landmark detection**, **autonomous navigation**, **obstacle avoidance**, and **speech feedback** within ROS 2.

Instead of relying on manual control, users select destinations through simple hand gestures while the robot plans and executes a path using Nav2. QR codes are used to verify arrival at important locations during navigation.

The system demonstrates a more intuitive approach to indoor human-robot interaction, while revealing limitations related to camera accuracy, lighting, processing speed, and environmental change.

</td>
<td width="40%" valign="top">

**Gesture Recognition**
Detects 21 hand landmarks from RGB camera frames and classifies gestures based on finger positions using Mediapipe Hands.

<br/>

**Autonomous Navigation**
Nav2 with A\* path planning, LiDAR-based localization, and real-time obstacle avoidance via the RPLIDAR A1.

<br/>

**Speech Feedback**
QR codes verify landmark arrival and trigger spoken tour descriptions on the connected host machine.

</td>
</tr>
</table>

---

## Poster

<div align="center">

[![Download Poster PDF](https://img.shields.io/badge/Download_Poster_PDF-700000?style=for-the-badge&logoColor=FDF9D8)](https://github.com/user-attachments/files/27560242/robotics.pdf)

<br/>

[![Poster Preview](https://github.com/user-attachments/assets/c2ec3130-6986-4614-9e79-cee726147861)](https://github.com/user-attachments/files/27560242/robotics.pdf)

</div>

---

## Hardware

| Component | Role |
|-----------|------|
| OAK-D Pro Stereo Camera | Gesture recognition and QR detection |
| 2D LiDAR (RPLIDAR A1) | Mapping, localization, and obstacle avoidance |
| Raspberry Pi 4 (4GB) | Onboard computation |
| Create 3 Drive Base | Differential drive with encoders, IMU, and safety sensors |

<br/>

<table>
<tr>
<td width="50%" valign="top">

**Person Detection**

- Detects and tracks the largest person in frame
- Bounding box center maps to angular velocity
- Bounding box size maps to distance estimation

</td>
<td width="50%" valign="top">

**LiDAR Perception**

- Provides real-time distance measurements to obstacles
- Used for SLAM map building, localization, and avoidance

</td>
</tr>
</table>

---

## System Pipeline

<div align="center">

| Gesture Input | ROS 2 | Navigation Goal | A\* Planning | LiDAR Avoidance | QR Detection | Speech Output |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Mediapipe reads finger count | Publishes navigation command | Goal sent to Nav2 | Optimal path computed | Localize and avoid obstacles | Scan QR at landmark | TTS confirms arrival |

</div>

---

## Three Phases

<table>
<tr>

<td width="33%" valign="top">

### Phase 1 — Mapping

Drive the robot through the target environment using keyboard teleop. SLAM Toolbox builds a 2D LiDAR occupancy map in real time. The completed map is saved as `.yaml` and `.pgm` files.

```bash
./start_mapping.sh
```

</td>

<td width="33%" valign="top">

### Phase 2 — Landmarking

Load the saved map and manually drive to each tour stop. Register up to three landmark positions plus a home position, saved to `landmarks.yaml`.

```bash
./start_landmarks.sh
```

</td>

<td width="33%" valign="top">

### Phase 3 — Autonomous Tour

The robot detects and follows a person, reads their gesture input, navigates via A\* to the selected landmark, scans the QR code, and delivers spoken output. The loop repeats continuously.

```bash
./start_person_follow.sh
```

</td>

</tr>
</table>

---

## Gesture Reference

<div align="center">

| Fingers Shown | Destination |
|:---:|:---:|
| 1 | Landmark 1 |
| 2 | Landmark 2 |
| 3 | Landmark 3 |
| 4 | Return Home |

</div>

QR codes at each stop should encode `task1`, `task2`, or `task3`. After scanning, the robot rotates approximately 180 degrees to face the visitor.

---

## Setup

> For the complete step-by-step manual see [manual_guide.md](manual_guide.md).

**1. Clone and build**
```bash
git clone https://github.com/Fnorgh/Turtlebot4-TourGuide.git
cd Turtlebot4-TourGuide/ros2_ws
colcon build --packages-select topological_nav
```

**2. Python environment**
```bash
~/.local/bin/virtualenv --system-site-packages venv
venv/bin/pip install -r requirements.txt ultralytics "numpy<2"
```

**3. Configure robot connection**
```bash
ssh student@<robot-name>.cs.nor.ou.edu
printf "<robot_name>" | robot-setup.sh
# Copy ROBOT_NAME, ROS_DOMAIN_ID, ROS_DISCOVERY_SERVER into the top of each .sh script
```

Valid robot names: `snapper` `loggerhead` `testudo` `galapagos` `terrapin` `leatherback` `hawksbill` `matamata` `softshell`

**4. Run**
```bash
chmod +x start_mapping.sh start_landmarks.sh start_person_follow.sh
./start_mapping.sh
```

---

## Results

- Gesture-based control functioning end-to-end across all four commands
- Autonomous navigation via Nav2 with A\* path planning
- QR landmark verification at each registered stop
- Full system pipeline integration across perception, planning, and feedback
- SLAM LiDAR map building in structured indoor environments

---

## Discussion

| Challenge | Notes |
|-----------|-------|
| Hardware constraints | Onboard Raspberry Pi 4 limited the ability to run YOLOv8 and gesture recognition simultaneously |
| QR detection | Reliability dependent on distance and camera viewing angle |
| Person-following | Performance degrades in crowded or visually noisy environments |
| Navigation consistency | Slow or inconsistent behavior due to frequent pose adjustments and conservative movement updates |
| Landmark navigation | Relies on manually defined positions rather than dynamic scene understanding |

---

## Future Work

- Improve gesture recognition accuracy using more robust deep learning models
- Replace QR landmark codes with semantic scene understanding
- Optimize the perception pipeline for real-time multi-model execution
- Enhance system adaptability to dynamic and unstructured environments

---

## Team

**University of Oklahoma — Robotics Course Project**

<div align="center">

<img src="https://github.com/user-attachments/assets/acbf6701-caab-4ca0-b840-ec71fb1e0c76" width="500" />

Nicholas Louque · Noah Gibson · Jace Rausch

</div>

---

## References

- [ROS 2 Documentation](https://docs.ros.org)
- [Nav2 Navigation Stack](https://nav2.ros.org)
- [MediaPipe Hands — Google](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [YOLOv8 Object Detection — Ultralytics](https://docs.ultralytics.com)

---
