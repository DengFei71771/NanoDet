import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/df/nanodet_ROS2humble/install/ros2_nanodet'
