import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import random
import math

class LidarPatternPublisher(Node):
    def __init__(self):
        super().__init__('lidar_pattern_publisher')
        self.publisher_ = self.create_publisher(LaserScan, '/turtle1/scan', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)

        self.scenarios = {
            "FRONT_BLOCK": {"center": 0, "width": 40, "dist": 0.5},
            "LEFT_WALL":   {"center": 90, "width": 60, "dist": 0.7},
            "RIGHT_WALL":  {"center": 270, "width": 60, "dist": 0.7},
            "CLEAR_PATH":  {"center": 0, "width": 0, "dist": 3.5} 음
        }
        
        self.get_logger().info('Lidar Scenario Publisher Started!')

    def timer_callback(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        
        msg.angle_min = 0.0
        msg.angle_max = math.radians(359)
        msg.angle_increment = math.radians(1)
        msg.range_min = 0.12
        msg.range_max = 3.5

        ranges = [3.5 for _ in range(360)]

        name, s = random.choice(list(self.scenarios.items()))
        
        half_w = s['width'] // 2
        if half_w > 0:
            for i in range(-half_w, half_w + 1):
                idx = (s['center'] + i) % 360
                ranges[idx] = s['dist']

        msg.ranges = ranges
        self.publisher_.publish(msg)
        self.get_logger().info(f'Current Scenario: [{name}] - Distance: {s["dist"]}m')

def main(args=None):
    rclpy.init(args=args)
    node = LidarPatternPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()