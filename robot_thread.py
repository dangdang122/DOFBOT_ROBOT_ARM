import time
import shared
from dofbot_simple import DofbotSimple


def run_robot_loop():

    bot = None

    try:

        bot = DofbotSimple("dofbot.urdf")

        while True:

            target_pos = None
            gripper_cmd = None
            torque_cmd = None

            with shared.cmd_lock:

                if shared.command["target_pos"] is not None:
                    target_pos = shared.command["target_pos"]
                    shared.command["target_pos"] = None

                if shared.command["gripper_cmd"] is not None:
                    gripper_cmd = shared.command["gripper_cmd"]
                    shared.command["gripper_cmd"] = None

                if shared.command["torque_cmd"] is not None:
                    torque_cmd = shared.command["torque_cmd"]
                    shared.command["torque_cmd"] = None


            if torque_cmd is not None:
                bot.set_torque(torque_cmd)


            if gripper_cmd is not None:
                bot.set_gripper(int(gripper_cmd))


            if target_pos is not None:

                if isinstance(target_pos,(list,tuple)):
                    x,y,z = target_pos

                elif isinstance(target_pos,dict):
                    x = target_pos["x"]
                    y = target_pos["y"]
                    z = target_pos["z"]

                bot.move_to_xyz(float(x),float(y),float(z))


            degrees = bot.sync_state_from_hardware()

            with shared.state_lock:

                shared.robot_state["x"] = bot.last_pos[0]
                shared.robot_state["y"] = bot.last_pos[1]
                shared.robot_state["z"] = bot.last_pos[2]

                shared.joints_degrees = degrees[:]

            time.sleep(0.05)

    finally:

        if bot is not None:
            bot.go_home()
