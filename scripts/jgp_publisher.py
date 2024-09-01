#!/usr/bin/env python3
# ROS2 libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
# Python libraries
import math

class JointGroupPositionPublisher(Node):
    def __init__(self):
        super().__init__('joint_group_position_publisher')

        self.final_position = math.radians(45)
        self.q = 0.0

        self.controller_topic = "/joint_group_position_controller/commands"
        self.controller_publisher = self.create_publisher(Float64MultiArray, self.controller_topic, 10)
         
        self.controller_msg = Float64MultiArray()
        self.position_timer = self.create_timer(0.5, self.publish_joint_position)
    
    def publish_joint_position(self):
        self.controller_msg.data = [
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q,
            self.q
        ]

        self.controller_publisher.publish(self.controller_msg)
        
        print("\nLeg's Joints:")
        print(f"\tQ1: {round(math.degrees(self.q), 2)} °")
        print(f"\tQ2: {round(math.degrees(self.q), 2)} °")
        print(f"\tQ3: {round(math.degrees(self.q), 2)} °")

        self.q += math.radians(3)

        if(self.q >= self.final_position):
             self.q = self.final_position

def main(args=None):
    rclpy.init(args=args)
    joint_angle_position_publisher_node = JointGroupPositionPublisher()
    try:
        rclpy.spin(joint_angle_position_publisher_node)
    except KeyboardInterrupt:
        joint_angle_position_publisher_node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()