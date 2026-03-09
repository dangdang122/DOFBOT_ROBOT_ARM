import time
import math
import os
from Arm_Lib import Arm_Device
import ikpy.chain


class DofbotSimple:

    def __init__(self, urdf_file_name):

        self.Arm = Arm_Device()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        urdf_path = os.path.join(current_dir, urdf_file_name)

        self.chain = ikpy.chain.Chain.from_urdf_file(
            urdf_path,
            active_links_mask=[False, True, True, True, True, True, False]
        )

        self.gripper_angle = 90
        self.last_pos = [0.0,0.0,0.0]
        self.last_joints = [0.0]*7

        self.sync_state_from_hardware()

    def sync_state_from_hardware(self):

        real_joints = [0.0]*7
        degrees = [0]*6

        for i in range(1,7):

            angle = self.Arm.Arm_serial_servo_read(i)

            if angle is None:
                angle = 90

            degrees[i-1] = angle

            if i <= 5:
                real_joints[i] = math.radians(angle - 90)

        self.gripper_angle = degrees[5]

        T = self.chain.forward_kinematics(real_joints)
        pos = T[:3,3]

        self.last_joints = real_joints
        self.last_pos = [pos[0],pos[1],pos[2]]

        return degrees

    def set_gripper(self,angle,duration_ms=1500):

        angle = int(max(10,min(170,angle)))

        if self.gripper_angle == angle:
            return

        self.gripper_angle = angle

        self.Arm.Arm_serial_servo_write(
            6,
            angle,
            int(duration_ms)
        )

    def move_to_xyz(self,x,y,z,duration_ms=1500):

        target_position = [x,y,z]

        ik_angles = self.chain.inverse_kinematics(
            target_position,
            orientation_mode=None
        )

        s1 = 90 + math.degrees(ik_angles[1])
        s2 = 90 + math.degrees(ik_angles[2])
        s3 = 90 + math.degrees(ik_angles[3])
        s4 = 90 + math.degrees(ik_angles[4])
        s5 = 90

        safe = [int(max(0,min(180,a))) for a in [s1,s2,s3,s4,s5]]

        self.Arm.Arm_serial_servo_write6(
            safe[0],
            safe[1],
            safe[2],
            safe[3],
            safe[4],
            self.gripper_angle,
            int(duration_ms)
        )

    def set_torque(self,val):

        self.Arm.Arm_serial_set_torque(int(val))

    def go_home(self):

        self.Arm.Arm_serial_servo_write6(
            90,90,90,90,90,
            self.gripper_angle,
            1000
        )

        time.sleep(1.5)
