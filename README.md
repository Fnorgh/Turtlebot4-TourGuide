

https://github.com/user-attachments/assets/7da67601-9a57-4d6e-9455-9c5c023634b7

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=700000&height=120&text=TurtleBot4%20Tour%20Guide&fontSize=40&fontColor=FDF9D8&fontAlignY=45&desc=Gesture-Controlled%20Landmark%20Navigation%20with%20ROS%202&descSize=15&descColor=e8d9a0&descAlignY=68" width="100%" />
<img src="https://placehold.co/1400x6/FDF9D8/FDF9D8" width="100%" />

<br/>


https://github.com/user-attachments/assets/22ac0e2a-f9b1-444d-b467-b6c9ec6cb7c2


<img src="https://readme-typing-svg.demolab.com?font=Georgia&size=15&duration=3500&pause=1200&color=FDF9D8&center=true&vCenter=true&width=700&lines=Gesture+Input+%E2%86%92+Nav2+%E2%86%92+A*+Path+Planning+%E2%86%92+QR+Detection+%E2%86%92+Speech+Output;OAK-D+Pro+Camera+%7C+RPLIDAR+A1+%7C+Raspberry+Pi+4+%7C+Create+3+Base;University+of+Oklahoma+%7C+Nicholas+Louque+%7C+Noah+Gibson+%7C+Jace+Rausch" />

<br/><br/>

![ROS2](https://img.shields.io/badge/ROS2_Humble-700000?style=flat-square&logo=ros&logoColor=FDF9D8)
![Python](https://img.shields.io/badge/Python_3.10+-700000?style=flat-square&logo=python&logoColor=FDF9D8)
![Mediapipe](https://img.shields.io/badge/Mediapipe-700000?style=flat-square&logoColor=FDF9D8)
![Nav2](https://img.shields.io/badge/Nav2-700000?style=flat-square&logoColor=FDF9D8)
![YOLOv8](https://img.shields.io/badge/YOLOv8-700000?style=flat-square&logoColor=FDF9D8)
![SLAM](https://img.shields.io/badge/SLAM_Toolbox-700000?style=flat-square&logoColor=FDF9D8)

<br/>

[![Watch Demo](https://img.shields.io/badge/Watch_Demo-FDF9D8?style=for-the-badge&logoColor=700000)](https://github.com/Fnorgh/Turtlebot4-TourGuide)
[![Read the Docs](https://img.shields.io/badge/Read_the_Docs-700000?style=for-the-badge&logoColor=FDF9D8)](https://github.com/Fnorgh/Turtlebot4-TourGuide/blob/main/manual_guide.md)

</div>

---

## Demo

<div align="center">

<!-- ================================================================
  HOW TO ADD YOUR VIDEO / PHOTO:

  Option A — Drag-and-drop video (recommended):
    1. Click the pencil icon to edit this README on GitHub
    2. Drag your .mp4 directly into the text editor
    3. GitHub generates a URL and pastes it in automatically

  Option B — GIF:
    <img src="YOUR_GIF_URL" width="100%" />
    Convert video to GIF free at https://ezgif.com

  Option C — Screenshot:
    Drag a .png/.jpg into the editor to get a hosted GitHub URL
================================================================ -->

<!-- DELETE this placeholder and paste your video or image URL below -->
<img src="https://placehold.co/800x400/700000/FDF9D8?text=Add+demo+video+or+image+here" width="100%" />

*Robot navigating to a registered landmark following gesture input — scanning the QR code and delivering spoken tour content.*

</div>

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

## Hardware

<table>
<tr>
<td width="50%" valign="top">

| Component | Role |
|-----------|------|
| OAK-D Pro Stereo Camera | Gesture recognition and QR detection |
| 2D LiDAR (RPLIDAR A1) | Mapping, localization, and obstacle avoidance |
| Raspberry Pi 4 (4GB) | Onboard computation |
| Create 3 Drive Base | Differential drive with encoders, IMU, and safety sensors |

</td>
<td width="50%" valign="top">

**Person Detection**
- Detects and tracks the largest person in frame
- Bounding box center maps to angular velocity
- Bounding box size maps to distance estimation

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

| Name | GitHub |
|------|--------|
| Nicholas Louque | [@Fnorgh](https://github.com/Fnorgh) |
| Noah Gibson | — |
| Jace Rausch | — |

---

## References

- [ROS 2 Documentation](https://docs.ros.org)
- [Nav2 Navigation Stack](https://nav2.ros.org)
- [MediaPipe Hands — Google](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [YOLOv8 Object Detection — Ultralytics](https://docs.ultralytics.com)

---

<div align="center">

<img src="https://placehold.co/1400x6/FDF9D8/FDF9D8" width="100%" />
<img src="https://capsule-render.vercel.app/api?type=rect&color=700000&height=60" width="100%" />

</div>
