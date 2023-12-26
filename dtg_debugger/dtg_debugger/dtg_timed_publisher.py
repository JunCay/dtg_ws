#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dtg_interfaces.msg import TcpString

class TimedPublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("Timed Publisher Initialized")
        self.timed_publisher_ = self.create_publisher(TcpString, "ether_msgs/test", 10)
        self.timer_interv = 2
        self.t_timer = self.create_timer(self.timer_interv, self.t_timer_callback)
        self.clock_ = self.get_clock()
        
    def t_timer_callback(self):
        msg = TcpString()
        now = self.clock_.now().seconds_nanoseconds()
        msg.stamp.sec = now[0]
        msg.stamp.nanosec = now[1]
        msg.content = "test content"
        msg.ip = "172.19.128.1"
        msg.port = 10110
        self.timed_publisher_.publish(msg)
        self.get_logger().info(f"tcp_msg published: {msg.content}")
        
        
def main(args=None):
    rclpy.init(args=args)
    node = TimedPublisher("dtg_timed_publisher")
    rclpy.spin(node)
    rclpy.shutdown()