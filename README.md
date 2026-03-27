가상 라이다 데이터를 이용하여 turtilsim을 자율주행 시키며 윈도우와 ros 통신 및 MYSQL과의 연동을 포함하는 프로그램입니다.

사용 방법
--우분투 터미널--
1. mkdir -p my_ws/src
2. cd my_ws/src
3. git clone https://github.com/kyujin1/turtle_sim_lidar.git
4. colcon build
5. source install/setup.bash
6. ros2 run turtlesim turtlesim_node                                 # turtlesim 실행 노드
7. ros2 launch rosbridge_server rosbridge_websocket_launch.xml       # roslibpy 브릿지 실행 노드
8. ros2 run turtle_lidar lidar_pub                                   # lidar 가상 데이터 발행


--윈도우 터미널--

window_turtle_lidar 디렉터리에 있는 파이썬 파일들을 실행합니다.
turtlesim_remote_control.py: 실시간 제어 및 데이터 저장용
turtlesim_db.py: 저장된 데이터를 분석 및 데이터프레임으로 변환용

주의 사항
turtlesim_db.py, turtlesim_remote_control.py 에 있는 host, user, password 는 본인에 맞게 수정하셔야 합니다.
