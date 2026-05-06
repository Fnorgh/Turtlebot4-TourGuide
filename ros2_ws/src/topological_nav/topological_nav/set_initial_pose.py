"""
Triggers AMCL global localization instead of a fixed initial pose.
Particles are spread across the entire map; AMCL converges as the robot moves.
"""
import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
import tf2_ros


class GlobalLocalizationNode(Node):

    def __init__(self):
        super().__init__('set_initial_pose')
        self.cli        = self.create_client(Empty, '/reinitialize_global_localization')
        self.tf_buffer  = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

    def map_tf_ready(self):
        try:
            self.tf_buffer.lookup_transform('map', 'base_link', rclpy.time.Time())
            return True
        except Exception:
            return False


def main(args=None):
    rclpy.init(args=args)
    node = GlobalLocalizationNode()

    print('Waiting for /reinitialize_global_localization service...')
    deadline = time.time() + 60.0
    while not node.cli.wait_for_service(timeout_sec=2.0):
        if time.time() > deadline:
            print('ERROR: AMCL service not available after 60 s')
            node.destroy_node()
            rclpy.shutdown()
            return
        print('  still waiting for AMCL...')

    print('Calling global localization — particles spread across entire map')
    future = node.cli.call_async(Empty.Request())
    rclpy.spin_until_future_complete(node, future, timeout_sec=10.0)
    print('Global localization initialized. Robot will self-localize as it moves.')

    print('Waiting for map→base_link TF...')
    deadline = time.time() + 60.0
    count = 0
    while time.time() < deadline:
        rclpy.spin_once(node, timeout_sec=0.2)
        if node.map_tf_ready():
            print(f'map→base_link TF confirmed. AMCL publishing.')
            break
        count += 1
        if count % 10 == 0:
            print(f'  still waiting for TF... ({count * 0.2:.0f}s)')
        time.sleep(0.2)
    else:
        print('Warning: map TF did not appear within 60 s')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
