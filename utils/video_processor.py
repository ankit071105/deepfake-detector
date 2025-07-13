import cv2
import numpy as np
from mtcnn import MTCNN

def extract_faces(video_path, max_frames=30):
    detector = MTCNN()
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        faces = detector.detect_faces(frame)
        if faces:
            x, y, w, h = faces[0]['box']
            face = frame[y:y+h, x:x+w]
            face = cv2.resize(face, (224, 224))
            frames.append(face)
    
    cap.release()
    return np.array(frames)

def process_video(video_path, model):
    frames = extract_faces(video_path)
    if len(frames) < 10:
        return {'prediction': 'INVALID', 'confidence': 0, 'message': 'Not enough faces detected'}
    
    # Preprocess frames
    frames = frames / 255.0
    frames = np.expand_dims(frames, axis=0)
    
    # Predict
    prediction = model.predict(frames)[0][0]
    is_fake = prediction > 0.5
    confidence = float(prediction if is_fake else 1 - prediction)
    
    return {
        'prediction': 'FAKE' if is_fake else 'REAL',
        'confidence': round(confidence * 100, 2),
        'message': 'This video appears to be authentic' if not is_fake else 'This video shows signs of manipulation'
    }