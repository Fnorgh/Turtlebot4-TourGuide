<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,60:1a3050,100:58a6ff&height=180&section=header&text=TurtleBot4%20Tour%20Guide&fontSize=40&fontColor=ffffff&fontAlignY=42&desc=Gesture-Controlled%20Landmark%20Navigation%20with%20ROS%202&descSize=15&descColor=8b949e&descAlignY=62" width="100%" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&duration=3000&pause=1000&color=58A6FF&center=true&vCenter=true&width=680&lines=Gesture+Input+%E2%86%92+Nav2+%E2%86%92+A*+Path+Planning+%E2%86%92+QR+Detection+%E2%86%92+Speech;OAK-D+Pro+%C2%B7+RPLIDAR+A1+%C2%B7+Raspberry+Pi+4+%C2%B7+Create+3;University+of+Oklahoma+%C2%B7+Nicholas+Louque+%C2%B7+Noah+Gibson+%C2%B7+Jace+Rausch" />

<br/><br/>

![ROS2](https://img.shields.io/badge/ROS2_Humble-22314e?style=for-the-badge&logo=ros&logoColor=58a6ff)
![Python](https://img.shields.io/badge/Python_3.10+-2c2a00?style=for-the-badge&logo=python&logoColor=e3b341)
![Mediapipe](https://img.shields.io/badge/Mediapipe-2d1b45?style=for-the-badge&logoColor=bc8cff)
![Nav2](https://img.shields.io/badge/Nav2-1f3a52?style=for-the-badge&logoColor=79c0ff)
![YOLOv8](https://img.shields.io/badge/YOLOv8-0d2d1a?style=for-the-badge&logoColor=3fb950)
![SLAM](https://img.shields.io/badge/SLAM_Toolbox-21262d?style=for-the-badge&logoColor=e6edf3)

<br/>

[![Watch Demo](https://img.shields.io/badge/▶_Watch_Demo-58a6ff?style=for-the-badge)](https://github.com/Fnorgh/Turtlebot4-TourGuide)
[![Read the Docs](https://img.shields.io/badge/📄_Read_the_Docs-21262d?style=for-the-badge)](https://github.com/Fnorgh/Turtlebot4-TourGuide/blob/main/manual_guide.md)

</div>

---

## 📽️ Demo

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

<!-- DELETE this line and paste your video/image below -->
<img src="https://placehold.co/800x400/0d1117/58a6ff?text=Drop+your+demo+video+or+GIF+here" width="100%" />

*Robot navigating to a landmark after reading a hand gesture — scanning the QR code and delivering the tour description aloud.*

</div>

---

## 📋 Abstract

<table>
<tr>
<td width="60%" valign="top">

This project presents a **multimodal navigation system** for a TurtleBot 4 that allows users to guide a robot through hand gestures. The system combines **gesture recognition**, **QR landmark detection**, **autonomous navigation**, **obstacle avoidance**, and **speech feedback** within ROS 2.

Instead of relying on manual control, users can select destinations through simple gestures while the robot plans and follows a path using Nav2. QR codes are used to verify important locations during navigation.

Overall, the system demonstrates a more intuitive approach to indoor human-robot interaction, while also revealing limitations related to camera accuracy, lighting, processing speed, and environmental changes.

</td>
<td width="40%" valign="top">

**👁️ Gesture recognition**
Detects 21 hand landmarks from RGB frames and classifies gestures based on finger positions using Mediapipe Hands.

<br/>

**🧭 Autonomous navigation**
Nav2 with A* path planning, LiDAR-based localization, and real-time obstacle avoidance.

<br/>

**📣 Speech feedback**
QR codes verify landmark arrival and trigger spoken tour descriptions on the host machine.

</td>
</tr>
</table>

---

## 🔧 Hardware

<table>
<tr>
<td width="50%" valign="top">

| Component | Role |
|-----------|------|
| **OAK-D Pro Stereo Camera** | Gesture recognition & QR detection |
| **2D LiDAR (RPLIDAR A1)** | Mapping, localization & obstacle avoidance |
| **Raspberry Pi 4 (4GB)** | Onboard computation |
| **Create 3 Drive Base** | Differential drive with encoders, IMU & safety sensors |

</td>
<td width="50%" valign="top">

**Person detection**
- Detects and tracks the largest person in frame
- Bounding box center → angular velocity
- Bounding box size → distance estimation

**LiDAR perception**
- Distance measurements to obstacles
- Used for mapping, localization, and avoidance

</td>
</tr>
</table>

---

## ⚙️ System Pipeline

<div align="center">

| 🖐️ Gesture Input | → | 📡 ROS 2 | → | 🎯 Nav Goal | → | 🔷 A\* Planning | → | 📡 LiDAR Avoid | → | 📷 QR Detect | → | 🔊 Speech |
|:---------------:|:-:|:--------:|:-:|:-----------:|:-:|:---------------:|:-:|:--------------:|:-:|:------------:|:-:|:---------:|
| Mediapipe reads finger count | | Publishes navigation command | | Destination goal sent to Nav2 | | A* finds optimal path | | LiDAR localizes & avoids obstacles | | Robot scans QR at landmark | | TTS confirms arrival |

</div>

---

## 🚀 Three Phases

<table>
<tr>

<td width="33%" align="center" valign="top">

### 🗺️ Phase 1 — Mapping

Drive the robot through the environment. SLAM Toolbox builds a 2D LiDAR occupancy map in real time. Save as `.yaml` + `.pgm`.

```bash
./start_mapping.sh
```

</td>

<td width="33%" align="center" valign="top">

### 📍 Phase 2 — Landmarking

Load the map and drive to each stop. Register up to 3 landmarks + home, saved to `landmarks.yaml`.

```bash
./start_landmarks.sh
```

</td>

<td width="33%" align="center" valign="top">

### 🤖 Phase 3 — Autonomous Tour

Robot follows a person, reads their gesture, navigates via A*, scans QR codes, and speaks. Loops indefinitely.

```bash
./start_person_follow.sh
```

</td>

</tr>
</table>

---

## 🖐️ Gesture Reference

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

> For the full step-by-step manual see [manual_guide.md](manual_guide.md).

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
# Copy ROBOT_NAME, ROS_DOMAIN_ID, ROS_DISCOVERY_SERVER into each .sh script
```

Valid robot names: `snapper` `loggerhead` `testudo` `galapagos` `terrapin` `leatherback` `hawksbill` `matamata` `softshell`

**4. Run**
```bash
chmod +x start_mapping.sh start_landmarks.sh start_person_follow.sh
./start_mapping.sh
```

---

## 📊 Results

- ✅ Gesture-based control working end-to-end
- ✅ Autonomous navigation via Nav2 + A* path planning
- ✅ QR landmark verification at each stop
- ✅ Full system pipeline integration
- ✅ SLAM LiDAR map building

---

## 💬 Discussion

| Challenge | Detail |
|-----------|--------|
| **Hardware constraints** | Limited ability to run YOLOv8 and gesture recognition simultaneously on the onboard Pi |
| **QR detection** | Dependent on distance and viewing angle |
| **Person-following** | Performance decreases in crowded or noisy environments |
| **Navigation** | Slow or inconsistent due to frequent pose adjustments and conservative movement updates |
| **Landmark navigation** | Relies on manually defined positions rather than dynamic scene understanding |

---

## 🔭 Future Work

- 🧠 Improve gesture recognition with more robust deep learning models
- 🏙️ Replace QR codes with semantic scene understanding
- ⚡ Optimize the perception pipeline for real-time multi-model execution
- 🌍 Enhance adaptability to dynamic and unstructured environments

---

## 👥 Team

**University of Oklahoma — Robotics Course Project**

| Name | GitHub |
|------|--------|
| Nicholas Louque | [@Fnorgh](https://github.com/Fnorgh) |
| Noah Gibson | — |
| Jace Rausch | — |

---

## 📚 References

- [ROS 2 Documentation](https://docs.ros.org)
- [Nav2 Navigation Stack](https://nav2.ros.org)
- [MediaPipe Hands — Google](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [YOLOv8 — Ultralytics](https://docs.ultralytics.com)

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:58a6ff,60:1a3050,100:0d1117&height=100&section=footer" width="100%" />

</div>
