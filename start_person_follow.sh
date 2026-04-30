#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  CHANGE THESE FOR YOUR ROBOT
# ─────────────────────────────────────────────
ROBOT_NAME="softshell"
ROS_DOMAIN_ID="9"
ROS_DISCOVERY_SERVER=";;;;;;;;;10.194.16.59:11811;"
# ─────────────────────────────────────────────

WS=~/robotics/ros2-topological-mapping-navigation/ros2_ws
REPO=~/robotics/ros2-topological-mapping-navigation
MAP=/home/louq0001/map.yaml

unset ROS_LOCALHOST_ONLY
export ROS_DOMAIN_ID=$ROS_DOMAIN_ID
export ROS_DISCOVERY_SERVER="$ROS_DISCOVERY_SERVER"
export ROS_SUPER_CLIENT=True
ros2 daemon stop; ros2 daemon start

ROS_ENV="unset ROS_LOCALHOST_ONLY && \
export ROS_DOMAIN_ID=$ROS_DOMAIN_ID && \
export ROS_DISCOVERY_SERVER=\"$ROS_DISCOVERY_SERVER\" && \
export ROS_SUPER_CLIENT=True && \
source $WS/install/setup.bash"

if [ ! -f "$MAP" ]; then
    echo "ERROR: $MAP not found. Run ./start_mapping.sh first."
    exit 1
fi

echo "==> Pulling latest changes..."
cd $REPO && git pull

echo "==> Building package..."
cd $WS && colcon build --base-paths src --packages-select topological_nav
source $WS/install/setup.bash

# ── Wait for robot to be reachable before starting nav stack ──────────────────
echo "==> Waiting for robot scan topic (confirms discovery server connected)..."
WAIT_LIMIT=60
WAITED=0
until timeout 2 ros2 topic hz /scan --window 1 2>/dev/null | grep -q "average rate"; do
    sleep 2
    WAITED=$((WAITED + 2))
    if [ $WAITED -ge $WAIT_LIMIT ]; then
        echo "WARNING: /scan not seen after ${WAIT_LIMIT}s — robot may not be reachable."
        echo "         Continuing anyway; nav2 may fail to localize."
        break
    fi
    echo "    ... still waiting for /scan ($WAITED s)"
done
echo "    Robot scan topic confirmed."

# ── Navigation stack (all-in-one) ─────────────────────────────────────────────
# localization_nav2.launch.py handles:
#   t=0s   → localization (map_server + AMCL)
#   t=25s  → set_initial_pose (waits for map TF up to 60 s)
#   t=90s  → nav2
echo "==> Starting navigation stack (one terminal)..."
gnome-terminal --title="Nav Stack" -- bash -c "
$ROS_ENV
ros2 launch topological_nav localization_nav2.launch.py map:=$MAP
exec bash"

# Wait for full nav2 activation:
#   90s (nav2 launch delay) + ~25s (lifecycle activation) = ~115s
echo "    Waiting 120 s for the full nav stack to activate..."
echo "    (localization t=0s, initial pose t=25s, nav2 t=90s)"
for i in $(seq 120 -10 10); do
    echo "    ... $i s remaining"
    sleep 10
done

# ── Person follow (state machine + YOLO + TTS) ────────────────────────────────
echo "==> Starting person follow launch..."
gnome-terminal --title="Person Follow" -- bash -c "
$ROS_ENV
ros2 launch topological_nav person_follow.launch.xml robot_name:=$ROBOT_NAME
exec bash"

sleep 2

gnome-terminal --title="Enable Follow" -- bash -c "
$ROS_ENV
echo 'Enabling person following...'
ros2 topic pub /person_follow_active std_msgs/Bool 'data: true'
exec bash"

gnome-terminal --title="QR Display" -- bash -c "
$ROS_ENV
ros2 run topological_nav qr_display_node
exec bash"

gnome-terminal --title="Speak Listener" -- bash -c "
$ROS_ENV
python3 $REPO/ros2_ws/src/topological_nav/topological_nav/speak_listener.py
exec bash"

echo ""
echo "==> All terminals launched."
echo "    Robot will follow a person."
echo "    Stop 5 s → show fingers: 1/2/3 = landmark, 4 = nearest, 5 = home."
