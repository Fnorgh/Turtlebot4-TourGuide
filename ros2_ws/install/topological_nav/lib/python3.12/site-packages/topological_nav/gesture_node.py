import sys
import os

_colcon_prefix = os.environ.get('COLCON_PREFIX_PATH', '')
if _colcon_prefix:
    _ws_root = os.path.dirname(_colcon_prefix.split(':')[0])
    _venv_sp = os.path.join(
        _ws_root, 'venv', 'lib',
        f'python{sys.version_info.major}.{sys.version_info.minor}',
        'site-packages',
    )
    if os.path.isdir(_venv_sp):
        sys.path.insert(0, _venv_sp)

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from collections import Counter
import mediapipe as mp
import time

GESTURE_NONE  = 0
GESTURE_ONE   = 1
GESTURE_TWO   = 2
GESTURE_THREE = 3
GESTURE_FOUR  = 4
GESTURE_FIVE  = 5
GESTURE_WAVE  = 10

FINGER_TIPS = [8, 12, 16, 20]   # index, middle, ring, pinky tip IDs
FINGER_PIPS = [6, 10, 14, 18]   # corresponding PIP joint IDs


class GestureNode(Node):

    def __init__(self):
        super().__init__('gesture_node')

        self.pub    = self.create_publisher(Int32, '/gesture', 10)
        self.bridge = CvBridge()
        self.create_subscription(
            Image, '/oakd/rgb/preview/image_raw', self.image_callback, 10)

        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )

        # Wave: track wrist x over recent frames
        self.wrist_x_history = []
        self.WAVE_WINDOW     = 15
        self.WAVE_THRESHOLD  = 0.20

        # Majority-vote buffer — publish when ≥ VOTES frames agree
        self.gesture_buffer = []
        self.BUFFER_LEN     = 20
        self.VOTES_NEEDED   = 17   # 17 out of 20 frames must agree (85%)

        # Cooldown per gesture
        self.last_published    = GESTURE_NONE
        self.last_publish_time = 0.0
        self.COOLDOWN_S        = 3.0

        self.get_logger().info('Gesture node ready — listening on /oakd/rgb/preview/image_raw')

    # ── Image callback ────────────────────────────────────────────────────────

    def image_callback(self, msg):
        frame  = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        result = self.hands.process(frame)

        gesture = GESTURE_NONE
        if result.multi_hand_landmarks:
            lm        = result.multi_hand_landmarks[0].landmark
            handedness = (result.multi_handedness[0].classification[0].label
                          if result.multi_handedness else 'Right')
            if self._is_wave(lm):
                gesture = GESTURE_WAVE
            else:
                count = self._count_fingers(lm, handedness)
                if 1 <= count <= 5:
                    gesture = count

        self._update_buffer(gesture)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _count_fingers(self, lm, handedness: str) -> int:
        # Count only the four fingers (index/middle/ring/pinky) — thumb ignored
        return sum(
            1 for tip, pip in zip(FINGER_TIPS, FINGER_PIPS)
            if lm[tip].y < lm[pip].y
        )

    def _is_wave(self, lm) -> bool:
        self.wrist_x_history.append(lm[0].x)
        if len(self.wrist_x_history) > self.WAVE_WINDOW:
            self.wrist_x_history.pop(0)
        if len(self.wrist_x_history) < self.WAVE_WINDOW:
            return False
        span = max(self.wrist_x_history) - min(self.wrist_x_history)
        return span > self.WAVE_THRESHOLD

    def _update_buffer(self, gesture):
        self.gesture_buffer.append(gesture)
        if len(self.gesture_buffer) > self.BUFFER_LEN:
            self.gesture_buffer.pop(0)

        if len(self.gesture_buffer) < self.BUFFER_LEN:
            return

        most_common, votes = Counter(self.gesture_buffer).most_common(1)[0]
        if most_common == GESTURE_NONE or votes < self.VOTES_NEEDED:
            return

        now = time.time()
        if most_common == self.last_published and \
                (now - self.last_publish_time) < self.COOLDOWN_S:
            return

        msg      = Int32()
        msg.data = most_common
        self.pub.publish(msg)
        self.last_published    = most_common
        self.last_publish_time = now
        self.get_logger().info(f'Gesture published: {most_common} ({votes}/{self.BUFFER_LEN} votes)')


def main(args=None):
    rclpy.init(args=args)
    node = GestureNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
