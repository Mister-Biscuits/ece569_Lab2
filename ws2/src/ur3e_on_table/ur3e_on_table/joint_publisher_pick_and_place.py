import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

# Length of one full pick-and-place cycle in seconds
CYCLE_TIME = 20.0


def linear_interpolate(p1, p2, a):
    return (1 - a) * p1 + a * p2


def blend_at(t):
    # Returns a in [0, 1] for time t in [0, CYCLE_TIME): 0 is p1, 1 is p2
    if t < 5.0:
        # 0..5 seconds: stay at p1
        return 0.0
    elif t < 10.0:
        # 5..10 seconds: move towards p2
        return (t - 5.0) / 5.0
    elif t < 15.0:
        # 10..15 seconds: stay at p2
        return 1.0
    else:
        # 15..20 seconds: move towards p1
        return 1.0 - (t - 15.0) / 5.0


class JointPublisherPickAndPlace(Node):

    def __init__(self):
        super().__init__('joint_publisher_pick_and_place')
        self.publisher_ = self.create_publisher(JointState, 'joint_states', 10)

        self.timer_period = 0.1  # seconds
        # Count whole timer ticks instead of summing floats, so the cycle never drifts
        self.steps_per_cycle = round(CYCLE_TIME / self.timer_period)
        self.i = 0
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # define your start/end points
        self.p1 = np.array([10.0, 13.0, 22.0, 31.0, 21.0, 13.0])
        self.p2 = np.array([11.0, 14.0, 23.0, 31.0, 21.0, 13.0])

    def timer_callback(self):
        t = self.i * self.timer_period
        a = blend_at(t)

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                    'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        msg.position = linear_interpolate(self.p1, self.p2, a).tolist()
        msg.velocity = []
        msg.effort = []

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing position: "{msg.position}"')

        # loop back to the beginning once the cycle is up
        self.i = (self.i + 1) % self.steps_per_cycle


def main(args=None):
    rclpy.init(args=args)

    joint_publisher_pick_and_place_node = JointPublisherPickAndPlace()

    rclpy.spin(joint_publisher_pick_and_place_node)

    joint_publisher_pick_and_place_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()