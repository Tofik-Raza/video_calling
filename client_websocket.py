import cv2
import base64
import socketio

# Initialize Socket.IO client
sio = socketio.Client()

# Server IP and port
server_url = "https://video-calling-0lkd.onrender.com"

@sio.event
def connect():
    print("Connected to server.")

@sio.event
def disconnect():
    print("Disconnected from server.")

def main():
    cap = cv2.VideoCapture(0)  # Open webcam
    sio.connect(server_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and encode frame to base64
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode(".jpg", frame)
        encoded_frame = base64.b64encode(buffer).decode("utf-8")

        # Send the encoded frame to the server
        try:
            sio.emit("send_frame", encoded_frame)
        except Exception as e:
            print(f"Error sending frame: {e}")
            break

    cap.release()
    sio.disconnect()

if __name__ == "__main__":
    main()
