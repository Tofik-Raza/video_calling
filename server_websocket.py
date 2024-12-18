from flask import Flask, Response
from flask_socketio import SocketIO, emit
import cv2
import base64
from waitress import serve


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["https://your-frontend-url.vercel.app"])
 # Allow all origins for testing

@app.route("/")
def index():
    return "WebSocket Video Server Running..."

# Event to handle video frame reception
@socketio.on("send_frame")
def handle_frame(data):
    try:
        # Decode the received frame
        frame_bytes = base64.b64decode(data)
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Broadcast frame back to all clients
        emit("receive_frame", {"frame": data}, broadcast=True)
        
        # Display the frame on the server for debugging
        if frame is not None:
            cv2.imshow("Server Video", frame)
            if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
                cv2.destroyAllWindows()
                socketio.stop()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    print("Starting production server...")
    serve(app, host="0.0.0.0", port=5000)