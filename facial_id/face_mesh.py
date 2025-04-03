import cv2
import mediapipe as mp
import time
import numpy as np

def track_eyes(countdown=3, output_path="eye_tracking.jpg"):
    # Initialize face mesh with eye refinement
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,  # Crucial for accurate eye tracking
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )

    # Precise eye landmark indices
    LEFT_EYE_INDICES = [33, 133, 144, 145, 153, 154, 155, 157, 158, 159]
    RIGHT_EYE_INDICES = [362, 263, 373, 374, 380, 381, 382, 384, 385, 386]

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    # Tracking variables
    eye_tracking_active = True
    start_countdown = False
    start_time = None
    eye_positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame capture error")
            break

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # Reset tracking data
        left_eye_points = []
        right_eye_points = []
        eye_detected = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w = frame.shape[:2]

                # Process left eye
                for idx in LEFT_EYE_INDICES:
                    landmark = face_landmarks.landmark[idx]
                    px, py = int(landmark.x * w), int(landmark.y * h)
                    left_eye_points.append((px, py))

                # Process right eye
                for idx in RIGHT_EYE_INDICES:
                    landmark = face_landmarks.landmark[idx]
                    px, py = int(landmark.x * w), int(landmark.y * h)
                    right_eye_points.append((px, py))

                # Calculate eye centers
                if left_eye_points and right_eye_points:
                    eye_detected = True
                    left_center = tuple(map(int, np.mean(left_eye_points, axis=0)))
                    right_center = tuple(map(int, np.mean(right_eye_points, axis=0)))
                    
                    # Store positions for tracking
                    eye_positions.append((left_center, right_center))

                    # Draw eye centers and connections
                    cv2.circle(frame, left_center, 5, (0, 255, 0), -1)
                    cv2.circle(frame, right_center, 5, (0, 255, 0), -1)
                    cv2.line(frame, left_center, right_center, (255, 0, 0), 2)

        # Countdown and capture logic
        if start_countdown:
            elapsed = time.time() - start_time
            remaining = countdown - int(elapsed)
            
            if remaining > 0:
                cv2.putText(frame, f"Capture in {remaining}s", (20, 40), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if eye_detected:
                    cv2.imwrite(output_path, frame)
                    print(f"Eye tracking captured: {output_path}")
                else:
                    print("No eyes detected in final frame!")
                break
        else:
            status_color = (0, 255, 0) if eye_detected else (0, 0, 255)
            cv2.putText(frame, "Press SPACE when ready", (20, 40), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

        cv2.imshow("Eye Tracking System", frame)
        
        key = cv2.waitKey(1)
        if key == 27:  # ESC to exit
            break
        elif key == 32:  # SPACE to start capture
            if eye_detected:
                start_countdown = True
                start_time = time.time()
            else:
                print("Cannot start - eyes not detected!")

    cap.release()
    cv2.destroyAllWindows()

# Run the eye tracker
track_eyes()




