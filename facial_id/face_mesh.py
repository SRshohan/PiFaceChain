import cv2
import mediapipe as mp

def draw_landmarks_on_camera():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)  # Open the default camera

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            break

        # Convert frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # Draw landmarks if detected
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    h, w, _ = frame.shape
                    x = int(landmark.x * w)  # Convert normalized x to pixel
                    y = int(landmark.y * h)  # Convert normalized y to pixel
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Draw dot

        # Show the frame
        cv2.imshow("3D Facial Landmarks", frame)

        # Exit on pressing the ESC key
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Call the function
draw_landmarks_on_camera()
