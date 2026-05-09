<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,60:1a3050,100:58a6ff&height=180&section=header&text=TurtleBot4%20Tour%20Guide&fontSize=40&fontColor=ffffff&fontAlignY=42&desc=Autonomous%20gesture-controlled%20tour%20guide%20robot&descSize=16&descColor=8b949e&descAlignY=62" width="100%" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=650&lines=Person+detection+%E2%86%92+Follow+%E2%86%92+Gesture+%E2%86%92+Navigate+%E2%86%92+QR+scan+%E2%86%92+Speak;Built+with+ROS2+%C2%B7+YOLOv8+%C2%B7+Nav2+%C2%B7+Mediapipe;University+of+Oklahoma+%C2%B7+Robotics+Course+Project" />

<br/><br/>

![ROS2](https://img.shields.io/badge/ROS2_Humble-22314e?style=for-the-badge&logo=ros&logoColor=58a6ff)
![Python](https://img.shields.io/badge/Python_3.10+-2c2a00?style=for-the-badge&logo=python&logoColor=e3b341)
![YOLOv8](https://img.shields.io/badge/YOLOv8-0d2d1a?style=for-the-badge&logoColor=3fb950)
![Nav2](https://img.shields.io/badge/Nav2-1f3a52?style=for-the-badge&logoColor=79c0ff)
![Mediapipe](https://img.shields.io/badge/Mediapipe-2d1b45?style=for-the-badge&logoColor=bc8cff)
![SLAM](https://img.shields.io/badge/SLAM_Toolbox-21262d?style=for-the-badge&logoColor=e6edf3)

<br/>

[![Demo Video](https://img.shields.io/badge/▶_Watch_Demo-58a6ff?style=for-the-badge)](https://github.com/Fnorgh/Turtlebot4-TourGuide)
[![Manual Guide](https://img.shields.io/badge/📄_Read_the_Docs-21262d?style=for-the-badge)](https://github.com/Fnorgh/Turtlebot4-TourGuide/blob/main/manual_guide.md)

</div>

---

## 📽️ Demo

<div align="center">

<!-- ================================================================
  HOW TO ADD YOUR VIDEO / PHOTO:

  Option A — Drag-and-drop video (recommended):
    1. Click the pencil icon to edit this README on GitHub
    2. Drag your .mp4 file directly into the text editor
    3. GitHub generates a link — it replaces this comment automatically

  Option B — GIF:
    <img src="YOUR_GIF_URL" width="100%" />
    Convert video to GIF free at https://ezgif.com

  Option C — Screenshot:
    <img src="YOUR_IMAGE_URL" width="100%" />
    Drag a .png/.jpg into the editor to get a hosted URL
================================================================ -->

<!-- DELETE THIS LINE and paste your video/image below it -->
<img src="https://placehold.co/800x400/0d1117/58a6ff?text=Drop+your+demo+video+or+GIF+here" width="100%" />

*Robot navigating to Landmark 2 after reading a ✌️ gesture — scanning the QR code and delivering the tour description aloud.*

</div>

---

## 📋 Abstract

<table>
<tr>
<td width="60%" valign="top">

This project presents an autonomous tour guide robot built on a **TurtleBot 4** platform. The system combines real-time computer vision, gesture recognition, and autonomous navigation to create a hands-free, interactive tour experience.

A visitor approaches the robot, which detects and follows them using **YOLOv8** person detection. When close enough, the robot stops and waits. The visitor holds up fingers (1–4) to select a destination. **Nav2** handles the routing, and at each landmark the robot scans a **QR code** and speaks the associated tour content aloud through the host machine.

The robot operates across three sequential phases: mapping the environment with **SLAM**, registering landmark positions, then running fully autonomously — looping through detection, gesture input, navigation, and speech indefinitely.

</td>
<td width="40%" valign="top">

**👁️ Real-time perception**
YOLOv8n person detection + Mediapipe gesture recognition running on the robot's live camera feed.

<br/>

**🗺️ Autonomous navigation**
SLAM-built 2D occupancy maps, Nav2 path planning, topological landmark waypoints stored in YAML.

<br/>

**📣 Audio tour delivery**
QR code scanning at each stop triggers text-to-speech output on the connected host machine.

</td>
</tr>
</table>

---

## ⚙️ System Pipeline

<div align="center">

| 🧍 Detect | → | 🏃 Follow | → | 🖐️ Gesture | → | 🧭 Navigate | → | 📷 QR Scan | → | 🔊 Speak |
|:---------:|:-:|:---------:|:-:|:----------:|:-:|:-----------:|:-:|:----------:|:-:|:--------:|
| YOLOv8n finds a person in frame | | Robot approaches and stops at threshold distance | | Mediapipe reads 1–4 fingers from camera | | Nav2 routes to the selected landmark | | Robot rotates to scan QR at the stop | | TTS plays tour description on host |

</div>

---

## 🚀 Three Phases

<table>
<tr>

<td width="33%" align="center" valign="top">

### 🗺️ Phase 1 — Mapping

Drive the robot through the environment using keyboard teleop. SLAM Toolbox builds a 2D occupancy map in real time. Save the finished map as `.yaml` + `.pgm`.

```bash
./start_mapping.sh
```

</td>

<td width="33%" align="center" valign="top">

### 📍 Phase 2 — Landmarking

Load the saved map and drive to each tour stop. Register up to 3 landmarks + home, then save positions to `landmarks.yaml`.

```bash
./start_landmarks.sh
```

</td>

<td width="33%" align="center" valign="top">

### 🤖 Phase 3 — Autonomous Tour

Robot follows visitors, reads gestures, navigates to landmarks, scans QR codes, and speaks tour descriptions. Fully autonomous loop.

```bash
./start_person_follow.sh
```

</td>

</tr>
</table>

---

## 🖐️ Gesture Reference

Show fingers to the camera to navigate:

<div align="center">

| Gesture | Destination |
|:-------:|:-----------:|
| ☝️ 1 finger | Landmark 1 |
| ✌️ 2 fingers | Landmark 2 |
| 🤟 3 fingers | Landmark 3 |
| 🖖 4 fingers | Return Home |

</div>

QR codes at each stop should encode `task1`, `task2`, or `task3`. After scanning, the robot rotates ~180° to face the visitor again.

---

## 🛠️ Quick Setup

> For the full manual walkthrough see [manual_guide.md](manual_guide.md).

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

**3. Configure your robot**
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

## 👥 Team

University of Oklahoma — Robotics Course Project

<!-- Fill in your team:
| Name | GitHub | Role |
|------|--------|------|
| Your Name | @handle | Navigation & SLAM |
| Teammate | @handle | Vision & Gestures |
-->

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:58a6ff,60:1a3050,100:0d1117&height=100&section=footer" width="100%" />

</div>
