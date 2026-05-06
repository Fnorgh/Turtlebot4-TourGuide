import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import subprocess
import time


SCAN_TIMEOUT = 60.0   # seconds before giving up

LANDMARK_SCRIPTS = {
    'task1': (
        "Bizzell Memorial Library. "
        "Bizzell Memorial Library is one of the most recognizable and historically significant "
        "buildings on campus. Built in 1929, it stands as a symbol of academic life at OU, "
        "with its red brick exterior and Collegiate Gothic architecture reflecting the "
        "university's long-standing traditions. The library was named in honor of William "
        "Bennett Bizzell, a former university president who played a major role in shaping "
        "OU's academic identity. "
        "Inside, the Great Reading Room is often considered the heart of the building. "
        "With its high vaulted ceilings, large windows, and rows of wooden desks, it creates "
        "a quiet and inspiring atmosphere for studying. The space feels almost cathedral-like, "
        "emphasizing the importance of knowledge and scholarship. Over the years, Bizzell "
        "Library has expanded to include modern research facilities while still preserving "
        "its historic character, making it a blend of past and present."
    ),
    'task2': (
        "Evans Hall, The Clock Tower. "
        "Evans Hall is best known for its tall clock tower, which has become a defining "
        "feature of the OU skyline. Completed in 1954, Evans Hall primarily houses classrooms "
        "and faculty offices, especially for math and science departments. Its height and "
        "central location make it easy to spot from almost anywhere on campus. "
        "The clock tower itself serves as both a practical and symbolic landmark. Students "
        "often use it as a meeting point, and it helps orient visitors navigating the "
        "university grounds. At different times of day, especially during sunrise or sunset, "
        "the tower stands out dramatically against the Oklahoma sky, making it a favorite "
        "subject for photos. For many students, Evans Hall becomes associated with challenging "
        "courses and long study sessions, making it an unforgettable part of their academic journey."
    ),
    'task3': (
        "The South Oval. "
        "South Oval is the scenic and social heart of the OU campus. Lined with trees and "
        "wide walkways, it connects many of the university's most important buildings and "
        "serves as a central gathering place for students, faculty, and visitors. Throughout "
        "the year, the South Oval transforms with the seasons, from vibrant green in the "
        "summer to colorful leaves in the fall. "
        "Beyond its beauty, the South Oval plays a major role in campus life. It's where "
        "students relax between classes, campus organizations set up events, and traditions "
        "unfold. The space encourages a sense of community, making it more than just a "
        "walkway. It's a place where everyday college experiences happen. Whether it's a "
        "quiet walk to class or a busy afternoon filled with activity, the South Oval "
        "captures the energy and spirit of OU."
    ),
}


def _speak(text: str):
    for cmd in (['spd-say', '-w', text], ['espeak', '-s', '140', text]):
        try:
            subprocess.run(cmd, timeout=120)
            return
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    print(f'*** {text} ***', flush=True)


class QRNode(Node):

    def __init__(self):
        super().__init__('qr_node')

        self.pub = self.create_publisher(String, '/qr_detected', 10)

        self.create_subscription(
            Image, '/oakd/rgb/preview/image_raw', self.image_callback, 10)

        self.bridge      = CvBridge()
        self.detector    = cv2.QRCodeDetector()
        self.done        = False
        self.start_time  = time.time()

        self.get_logger().info('QR node ready — scanning (60 s timeout)')

    def image_callback(self, msg):
        if self.done:
            return

        if time.time() - self.start_time > SCAN_TIMEOUT:
            self.get_logger().warn('QR scan timed out after 60 s')
            self.done = True
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        data, _, _ = self.detector.detectAndDecode(frame)

        if data:
            self.done = True
            self.get_logger().info(f'QR detected: {data}')

            script = LANDMARK_SCRIPTS.get(data, data)
            _speak(script)

            # Notify state machine
            out = String()
            out.data = data
            self.pub.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = QRNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
