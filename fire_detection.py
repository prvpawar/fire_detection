import cv2
import numpy as np
import os
import threading

def play_sound():
    os.system("start alert.wav")

cap = cv2.VideoCapture(0)
sound_on = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 🔥 Lighter / Matchstick Flame HSV range
    lower_flame = np.array([15, 120, 150])
    upper_flame = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_flame, upper_flame)

    # Noise remove
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fire_detected = False

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # 🔥 Lighter flame priority (small but intense)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)

            # Flame shape check (height > width)
            if h > w:
                fire_detected = True
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
                cv2.putText(frame, "🔥 LIGHTER FIRE DETECTED 🔥",
                            (20,40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,0,255), 3)
                break

    if fire_detected:
        if not sound_on:
            sound_on = True
            threading.Thread(target=play_sound, daemon=True).start()
    else:
        sound_on = False

    cv2.imshow("Fire Detection - Lighter Priority", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
