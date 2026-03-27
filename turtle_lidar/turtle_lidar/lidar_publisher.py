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

        # 고정 패턴 정의 (딕셔너리)
        # "이름": (중심각도, 벽의너비, 벽까지의거리)
        self.scenarios = {
            "FRONT_BLOCK": {"center": 0, "width": 40, "dist": 0.5},
            "LEFT_WALL":   {"center": 90, "width": 60, "dist": 0.7},
            "RIGHT_WALL":  {"center": 270, "width": 60, "dist": 0.7},
            "CLEAR_PATH":  {"center": 0, "width": 0, "dist": 3.5} # 장애물 없음
        }
        
        self.get_logger().info('Lidar Scenario Publisher Started!')

    def timer_callback(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'
        
        # 기본 라이다 설정
        msg.angle_min = 0.0
        msg.angle_max = math.radians(359)
        msg.angle_increment = math.radians(1)
        msg.range_min = 0.12
        msg.range_max = 3.5

        # 1. 모든 범위를 최대 거리(3.5m)로 초기화
        ranges = [3.5 for _ in range(360)]

        # 2. 딕셔너리에서 무작위 시나리오 선택
        name, s = random.choice(list(self.scenarios.items()))
        
        # 3. 선택된 범위(Index)에 고정된 거리값 주입
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