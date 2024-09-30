import cv2
import numpy as np
import sounddevice as sd
import time

# Function to generate a simple tone
def play_sound(frequency=440, duration=1):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, sample_rate)
    sd.wait()

# Function for verbal alert (using text-to-speech or simple print)
def verbal_alert(message):
    print(message)  # Replace this with a TTS system if available

# Define color bounds for tracking (e.g., red)
lower_color = np.array([0, 120, 70])
upper_color = np.array([10, 255, 255])

# Define thresholds
danger_position_threshold = 400  # X position threshold
danger_speed_threshold = 10  # Speed threshold (pixels/frame)
min_size_threshold = 500  # Minimum contour area threshold

# Start capturing video
cap = cv2.VideoCapture(0)
previous_positions = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    current_positions = []

    for contour in contours:
        if cv2.contourArea(contour) > min_size_threshold:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            current_positions.append((center_x, center_y))

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # Check position threshold
            if center_x > danger_position_threshold:
                alert_message = "Alert: Object has crossed the danger position threshold!"
                print(alert_message)
                verbal_alert(alert_message)
                play_sound()

            # Check for speed detection
            if previous_positions:
                previous_center_x = previous_positions[-1][0]
                speed = abs(center_x - previous_center_x)

                if speed > danger_speed_threshold:
                    alert_message = "Alert: Object is moving too fast!"
                    print(alert_message)
                    verbal_alert(alert_message)
                    play_sound()

    if current_positions:
        previous_positions.append(current_positions[-1])
    if len(previous_positions) > 5:
        previous_positions.pop(0)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
