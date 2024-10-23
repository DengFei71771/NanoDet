import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/df/nanodet_ROS2humble/nanodet_py/install/ros2_nanodet'
