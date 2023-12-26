#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dtg_interfaces.msg import TcpString
import socket

class EtherCenter(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("EtherCenter Initialized")
        self.ether_subscriber_ = self.create_subscription(TcpString, "ether_msgs/test", self.ether_sub_callback, 10)
        self.connection_publisher_ = self.create_publisher(TcpString, "connection", 10)
        self.clock_ = self.get_clock()
        self.client_dict = {}
        
    def ether_sub_callback(self, msg):
        now = self.clock_.now().seconds_nanoseconds()
        content = msg.content
        ip = msg.ip
        port = msg.port
        addr = (ip, port)
        self.get_logger().info(f"TcpString msg get: {ip}:{port}")

        if addr in self.client_dict.keys():
            clientsocket = self.client_dict[addr]
        else:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                clientsocket.connect(addr)
            except:
                self.get_logger().info(f"Unexpected tcp msg, server has not started yet...")
                return
            self.connection_publisher_.publish(msg)
            self.get_logger().info(f"New client created, binding {ip}:{port} at time: {now[0]}")
            self.client_dict[addr] = clientsocket
            
        if "QUIT" in content:
            clientsocket.close()
            return
        
        try:
            clientsocket.sendall(content.encode())
        except:
            self.get_logger().info(f"send failed...")
        # while True:
        #     data = clientsocket.recv(1024).decode()
        #     self.get_logger().info(f"Received msg from server: {data}")
        #     if data[-1] == '\r':
        #         break
            
        
def main(args=None):
    rclpy.init(args=args)
    node = EtherCenter("dtg_ether_bridge")
    rclpy.spin(node)
    rclpy.shutdown()