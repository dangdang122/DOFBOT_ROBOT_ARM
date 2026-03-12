import threading

from app.websocket_server import create_app
from app.websocket_server.socketio_instance import socketio
from app.websocket_server.broadcaster import broadcast_data
from app.robot import robot_thread


app = create_app()


if __name__ == "__main__":

    t_robot = threading.Thread(
        target=robot_thread.run_robot_loop,
        daemon=True
    )
    t_robot.start()

    t_broadcast = threading.Thread(
        target=broadcast_data,
        daemon=True
    )
    t_broadcast.start()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )