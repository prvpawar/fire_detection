import cv2
import pygame

# 🔊 Pygame setup for WAV sound
pygame.mixer.init()
pygame.mixer.music.load("alert.wav")  # WAV file use kare

cap = cv2.VideoCapture(0)
sound_on = False

# Brightness detection parameters
THRESHOLD = 240     # brightness threshold
PIXEL_LIMIT = 1500  # number of bright pixels to trigger alert

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for performance
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔆 Detect bright areas
    _, bright = cv2.threshold(gray, THRESHOLD, 255, cv2.THRESH_BINARY)
    bright_pixels = cv2.countNonZero(bright)

    if bright_pixels > PIXEL_LIMIT:
        cv2.putText(
            frame,
            "FLASHLIGHT / FIRE DETECTED",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        # 🔊 Play WAV sound in background
        if not sound_on:
            pygame.mixer.music.play(-1)  # loop continuously
            sound_on = True
    else:
        # Stop sound when flash not detected
        if sound_on:
            pygame.mixer.music.stop()
            sound_on = False

    # Display camera feed
    cv2.imshow("Flashlight Alert System", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
