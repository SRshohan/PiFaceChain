import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmark_coords = []
            for idx, landmark in enumerate(face_landmarks.landmark):
                x = landmark.x  # Normalized (0 to 1)
                y = landmark.y  # Normalized (0 to 1)
                z = landmark.z  # Relative depth
                landmark_coords.append((x, y, z))
            
            print("3D Facial Landmarks:", landmark_coords)  # Print 3D landmarks

cap.release()
cv2.destroyAllWindows()