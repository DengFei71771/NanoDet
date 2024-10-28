#!/usr/bin/env python3
# 实现将nanodet python版本转换为ROS humble
import sys


import os
import time
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header
import nanodet_py.src.ros2_nanodet.ros2_nanodet.nanodet
from nanodet_py.src.ros2_nanodet.ros2_nanodet.nanodet import my_nanodet


IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

class NanoDetNode(Node):
    def __init__(self):
        super().__init__('ros_nanodet')

        model_dir = os.path.dirname(nanodet_py.src.ros2_nanodet.scripts.nanodet.__file__)
        model_path = os.path.join(model_dir, 'model/nanodet.onnx')
        clsname_path = os.path.join(model_dir, 'model/coco.names')

        self.nanodet_model = my_nanodet(model_path=model_path, clsname_path=clsname_path)
        self.image_pub = self.create_publisher(Image, '/nanodet_result_out', 1)

        self.create_subscription(Image, '/usb_cam/image_raw', self.image_callback_1, 1)

    def image_callback_1(self, image):
        ros_image = np.frombuffer(image.data, dtype=np.uint8).reshape(image.height, image.width, -1)[..., ::-1]
        nanodet_result_image = self.nanodet_model.detect(ros_image)
        cv2.imshow('nanodet_result', nanodet_result_image)
        cv2.waitKey(5)
        self.publish_image(nanodet_result_image)

    def publish_image(self, imgdata):
        image_temp = Image()
        header = Header(stamp=self.get_clock().now().to_msg())
        header.frame_id = 'map'
        
        image_temp.height = IMAGE_HEIGHT
        image_temp.width = IMAGE_WIDTH
        image_temp.encoding = 'rgb8'
        image_temp.data = np.array(imgdata).tobytes()
        image_temp.header = header
        image_temp.step = IMAGE_WIDTH * 3
        
        self.image_pub.publish(image_temp)

def main(args=None):
    rclpy.init(args=args)
    node = NanoDetNode("nanodet")
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
