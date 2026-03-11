from .socketio_instance import socketio
from ..robot import shared

@socketio.on('set_gripper')
def handle_set_gripper(data):
    if 'gripper' in data:
        with shared.cmd_lock:
            shared.command["gripper_cmd"] = data['gripper']


@socketio.on('set_pos')
def handle_set_pos(data):
    if 'pos' in data:
        with shared.cmd_lock:
            shared.command["target_pos"] = data['pos']


@socketio.on('set_torque')
def handle_set_torque(data):
    if 'torque' in data:
        with shared.cmd_lock:
            shared.command["torque_cmd"] = data['torque']