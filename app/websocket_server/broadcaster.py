from ..robot import shared
import time
from .socketio_instance import socketio

def broadcast_data():
    while True:
        robot_packet = {}

        with shared.state_lock:
            robot_packet['ee'] = shared.robot_state.copy()
            robot_packet['joints'] = shared.joints_degrees[:]

        try:
            socketio.emit(
                'robot_state',
                robot_packet
            )

        except Exception:
            pass

        time.sleep(0.05)
