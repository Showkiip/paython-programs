import cv2
import mediapipe as mp
import numpy as np
import winsound  # For sound alerts on Windows

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Start capturing video
cap = cv2.VideoCapture(0)

def alert():
    # Play a simple alert sound
    frequency = 1000  # Set Frequency To 1000 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Draw landmarks on the frame
        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Check for dangerous behaviors
        shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        hip_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        knee_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y

        # Determine if the person is bending excessively or falling
        bending_threshold = 0.1  # Threshold for bending forward
        falling_threshold = 0.15  # Threshold for falling

        if shoulder_y < hip_y - bending_threshold and hip_y < knee_y:
            print("Alert: Excessive bending detected!")
            alert()  # Trigger alert sound

        if hip_y > shoulder_y + falling_threshold:
            print("Alert: Potential fall detected!")
            alert()  # Trigger alert sound

    # Show the video feed
    cv2.imshow('Pose Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
