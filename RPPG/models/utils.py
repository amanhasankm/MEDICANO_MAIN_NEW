import cv2
import numpy as np

def extract_face_region(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return frame  # fallback
    x, y, w, h = faces[0]
    return frame[y:y+h, x:x+w]

def extract_rppg_signal(face_roi):
    resized = cv2.resize(face_roi, (50, 50))
    r, g, b = cv2.split(resized)
    return np.array([np.mean(r), np.mean(g), np.mean(b)])

def predict_stress(hrv):
    return "High" if hrv < 20 else "Normal" if hrv < 60 else "Relaxed"

def predict_emotion(frame):
    return "Neutral"  # Placeholder for real emotion classifier
