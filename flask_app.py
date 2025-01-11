from flask import Flask, render_template, Response
import cv2
import json
import threading
import time
from ultralytics import YOLO
from datetime import datetime
import pytz

app = Flask(__name__)

# Load YOLO model for number plate detection
plate_model = YOLO("plate_v11.pt")

# Load your custom character recognition model
character_model = YOLO("best_Sep.pt")

# Initialize the video capture object
video_stream = cv2.VideoCapture(1)  # Use 0 for webcam or provide video file path

# Shared list to store detected number plates
detected_plates = []
detected_plates_lock = threading.Lock()  # Lock for thread-safe access

# Nepal Timezone
nepal_tz = pytz.timezone('Asia/Kathmandu')

def save_detected_plates_to_json():
    """
    Save detected plates to a JSON file every 20 seconds.
    """
    while True:
        time.sleep(20)
        with detected_plates_lock:
            with open("detected_plates.json", "w") as file:
                json.dump(detected_plates, file, indent=4)
            print("Saved detected plates to detected_plates.json")

# Start a background thread for saving plates
threading.Thread(target=save_detected_plates_to_json, daemon=True).start()

def recognize_characters(plate_img):
    """
    Use the character recognition model to process the plate image
    and extract characters.
    """
    results = character_model.predict(plate_img, conf=0.45)
    characters = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            label = result.names[int(box.cls[0])]  # Class label (e.g., a character)
            characters.append(label)
    return "".join(characters)  # Combine detected characters

def detect_and_recognize_number_plate(frame):
    """
    Detect number plates and recognize characters in the detected plates.
    """
    results = plate_model.predict(frame, conf=0.45)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            label = result.names[int(box.cls[0])]   # Class label (e.g., "License")
            
            # Crop the license plate region
            plate_img = frame[y1:y2, x1:x2]
            if plate_img.size > 0:
                # Recognize characters in the cropped plate image
                recognized_text = recognize_characters(plate_img)
                label += f" [{recognized_text}]"

                # Save the recognized text with timestamp
                with detected_plates_lock:
                    timestamp = time.time()
                    timestamp_readable = datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(nepal_tz).strftime('%Y-%m-%d %H:%M:%S')
                    detected_plates.append({
                        "plate": recognized_text, 
                        "timestamp": timestamp,
                        "timestamp_readable": timestamp_readable
                    })

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def generate_frames():
    """
    A generator function to stream frames to the client.
    """
    while True:
        success, frame = video_stream.read()
        if not success:
            break
        # Process the frame with the detection and recognition models
        frame = detect_and_recognize_number_plate(frame)
        # Encode the frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame as a response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    with detected_plates_lock:
        # Passing detected plates to the HTML template
        plates_data = detected_plates[-5:]  # Show the last 5 plates
    return render_template('index.html', plates=plates_data)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
