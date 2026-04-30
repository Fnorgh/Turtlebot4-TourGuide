"""
Local speak listener — run this on your connecting computer (no sudo needed).
Subscribes to /speak and announces using spd-say, festival, or terminal bell.
Messages are queued and spoken in order without blocking the ROS2 executor.
"""
import queue
import subprocess
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def _tts(text: str):
    for cmd in (
        ['spd-say', '-w', text],
        ['espeak', '-s', '140', text],
        ['festival', '--tts'],
    ):
        try:
            if cmd[0] == 'festival':
                subprocess.run(cmd, input=text.encode(), timeout=15)
            else:
                subprocess.run(cmd, timeout=15)
            return
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    print(f'\a\n*** {text.upper()} ***\n', flush=True)


class SpeakListener(Node):

    def __init__(self):
        super().__init__('speak_listener')
        self._q = queue.Queue()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()
        self.create_subscription(String, '/speak', self._cb, 10)
        self.get_logger().info('speak_listener ready — listening on /speak')

    def _cb(self, msg: String):
        self.get_logger().info(f'Speaking: "{msg.data}"')
        self._q.put(msg.data)

    def _run(self):
        while True:
            text = self._q.get()
            _tts(text)
            self._q.task_done()


def main():
    rclpy.init()
    node = SpeakListener()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
