import roslibpy
import mysql.connector
import json
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'ros_data'
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except Exception as e:
    exit()

client = roslibpy.Ros(host='localhost', port=9090)

def start_logic():

    scan_listener = roslibpy.Topic(client, '/turtle1/scan', 'sensor_msgs/LaserScan')
    cmd_vel_talker = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/Twist')

    def scan_callback(message):
        ranges = message.get('ranges', [])
        if not ranges: return

        front_ranges = ranges[0:21] + ranges[339:360]
        left_ranges = ranges[60:121]
        right_ranges = ranges[240:301]

        dist_f = min(front_ranges) if front_ranges else 3.5
        dist_l = min(left_ranges) if left_ranges else 3.5
        dist_r = min(right_ranges) if right_ranges else 3.5

        move_msg = {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        current_action = ""

        if dist_f < 0.6:
            current_action = "backward"
            move_msg['linear']['x'] = -1.0
        elif dist_l < 0.8:
            current_action = "turn_right"
            move_msg['linear']['x'] = 0.5
            move_msg['angular']['z'] = -2.0
        elif dist_r < 0.8:
            current_action = "turn_left"
            move_msg['linear']['x'] = 0.5
            move_msg['angular']['z'] = 2.0
        else:
            current_action = "forward"
            move_msg['linear']['x'] = 2.0

        try:
            sql = "INSERT INTO lidardata (ranges, `when`, action) VALUES (%s, %s, %s)"
            val = (json.dumps(ranges), datetime.now(), current_action)
            cursor.execute(sql, val)
            conn.commit()
            print(f" DB 저장 완료: {current_action} (ID: {cursor.lastrowid})")
        except Exception as db_err:
            print(f" DB 저장 중 오류: {db_err}")

        cmd_vel_talker.publish(roslibpy.Message(move_msg))

    scan_listener.subscribe(scan_callback)

client.on_ready(start_logic)

try:
    client.run_forever()
except KeyboardInterrupt:
    print("\n[중단] 종료 중...")
    cursor.close()
    conn.close()
    client.terminate()