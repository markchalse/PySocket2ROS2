# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import random

import datetime

actions = {
    1:"walkfoward",
    2:"handsup",
    3:"turn_left",
    4:"turn_right",
    5:"handwave_left",
    6:"walkback",
    7:"shakelegleft",
    8:"shakelegright",
    9:"handwave_right",
}


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        #self.publisher_ = self.create_publisher(String, 'ros2_topic', 10)
        self.publisher_2 = self.create_publisher(String, 'test_dance', 10)
        timer_period = 0.25  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.action_delay = 2 #3s action delay
        self.action_time = int(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        self.action = actions[random.randint(1,9)]
        

    def timer_callback(self):
        #msg = String()
        #msg.data = 'Hello I am ros this is topic: %d' % self.i
        #self.publisher_.publish(msg)
        msg2 = String()

        #msg2.data = 'okok topic: %d' % self.i

        msg2.data = self.action
        self.publisher_2.publish(msg2)
        self.get_logger().info('Publishing: "%s"' % msg2.data)
        
        now = int(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        if now-self.action_time>self.action_delay:
            self.action_time = now
            self.action = actions[random.randint(1,9)]
        #self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
