import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import os

model_path = os.path.abspath("face_landmarker.task")

if not os.path.exists(model_path):
    print("Model file not found")
    exit()

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    output_face_blendshapes=True,  # Optional: For facial expressions
    output_facial_transformation_matrixes=True  # Optional: For 3D transformations
)

frame_count = 0

with FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps <= 0:
        fps = 30
    print(f"FPS: {fps}")
    
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(frame_count * (1000 / fps))
        
        # Detect face landmarks
        face_landmarker_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        # Draw landmarks and bounding box
        if face_landmarker_result.face_landmarks:
            for face_landmarks in face_landmarker_result.face_landmarks:
                # Calculate bounding box from landmarks
                x_coords = [landmark.x * frame.shape[1] for landmark in face_landmarks]
                y_coords = [landmark.y * frame.shape[0] for landmark in face_landmarks]
                
                min_x = int(min(x_coords))
                max_x = int(max(x_coords))
                min_y = int(min(y_coords))
                max_y = int(max(y_coords))
                
                # Draw bounding box
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
                
                # Draw facial landmarks (optional)
                for landmark in face_landmarks:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow("Face Detection", frame)
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    
    