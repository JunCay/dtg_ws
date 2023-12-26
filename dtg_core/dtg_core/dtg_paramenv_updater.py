#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dtg_interfaces.msg import ParamEnv
from dtg_interfaces.msg import TcpString


class ParamEnvUpdater(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("ParamEnvUpdater Initialized")
        self.param_env = ParamEnv()
        
        self.connection_subscriber_ = self.create_subscription(TcpString, "connection", self.connection_callback, 10)
        self.paramenv_publisher_ = self.create_publisher(ParamEnv, "param_env", 10)
        self.timer_intv = 0.1
        
        self.clock_ = self.create_timer(self.timer_intv, self.timer_callback)
        
    def connection_callback(self, msg):
        ip = msg.ip
        port = msg.port
        link = ip + ':' + str(port)
        if link not in self.param_env.current_connection:
            self.param_env.current_connection.append(link)
        
    def param_update(self):
        pass
        
    def timer_callback(self):
        self.param_update()
        self.paramenv_publisher_.publish(self.param_env)
        
                 
def main(args=None):
    rclpy.init(args=args)
    node = ParamEnvUpdater("dtg_paramenv_updater")
    rclpy.spin(node)
    rclpy.shutdown()