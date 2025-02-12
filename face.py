import cv2
from deepface import DeepFace
import mediapipe as mp
import numpy as np
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Initialize Mediapipe face detection and drawing utilities
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Define focus and distraction conditions based on emotions
FOCUSED_EMOTIONS = ['neutral', 'happy']
DISTRACTED_EMOTIONS = ['sad', 'angry', 'disgust', 'fear', 'surprise']

# Initialize previous state variable
prev_state = "Focused"

# Function to call AutoHotkey script to throttle or restore network speed
def throttle_network(status):
    global prev_state
    if status == "Distracted" and prev_state == "Focused":
        prev_state = "Distracted"
        subprocess.call(["C:\\Program Files\\AutoHotkey\\v2\\AutoHotkey.exe", "C:\\Users\\MANAV\\OneDrive\\Documents\\throttle.ahk"])
    elif status == "Focused" and prev_state == "Distracted":
        prev_state = "Focused"
        # Add code to restore network speed if needed
        subprocess.call(["C:\\Program Files\\AutoHotkey\\v2\\AutoHotkey.exe", "C:\\Users\\MANAV\\OneDrive\\Documents\\restore.ahk"])
    # If the status does not change, do nothing


async def analyze_emotion(face_image):
    temp_path = "temp_face.jpg"
    cv2.imwrite(temp_path, face_image)
    analysis = await asyncio.get_event_loop().run_in_executor(
        ThreadPoolExecutor(), DeepFace.analyze, temp_path, ['emotion'], False
    )
    return analysis[0]['dominant_emotion']

def main():
    global prev_state
    # Open video capture (webcam)
    cap = cv2.VideoCapture(0)
    
    # Set up variables to manage analysis frequency
    last_analysis_time = time.time()
    analysis_interval = 2  # Analyze every 2 seconds

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            if results.detections and (time.time() - last_analysis_time) >= analysis_interval:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    
                    face_image = frame[y:y+h, x:x+w]

                    # Run emotion analysis asynchronously
                    loop = asyncio.get_event_loop()
                    emotion = loop.run_until_complete(analyze_emotion(face_image))

                    if emotion in FOCUSED_EMOTIONS:
                        print("Focused")
                        throttle_network("Focused")  # Call AutoHotkey for normal speed
                    elif emotion in DISTRACTED_EMOTIONS:
                        print("Distracted")
                        throttle_network("Distracted")  # Call AutoHotkey for reduced speed

                last_analysis_time = time.time()

            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
