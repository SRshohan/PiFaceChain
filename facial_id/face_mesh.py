import cv2
import mediapipe as mp
import time

def draw_landmarks_on_camera(countdown=5, output_path="captured.jpg"):
    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Open the default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    landmarks_active = True  # Initially, landmarks are active
    start_countdown = False  # Flag to start the countdown
    start_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            break

        # Process landmarks if active
        if landmarks_active:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    h, w, _ = frame.shape
                    for landmark in face_landmarks.landmark:
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Draw landmark dots
            cv2.putText(frame, "Press 'L' if you are ready to take picture", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Start the countdown
        if start_countdown:
            remaining_time = int(countdown - (time.time() - start_time))
            if remaining_time >= 0:
                cv2.putText(frame, f"Taking picture in {remaining_time}s...", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Save the final frame and exit the loop
                cv2.imwrite(output_path, frame)
                print(f"Picture saved as {output_path}")
                break

        # Show the feed
        cv2.imshow("Camera Feed", frame)

        # Key press handling
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key to exit
            break
        elif key == ord('l') and landmarks_active:  # Press 'L' to toggle landmarks off
            landmarks_active = False
            start_countdown = True
            start_time = time.time()  # Start the countdown timer

    cap.release()
    cv2.destroyAllWindows()

# # Call the function
# draw_landmarks_on_camera(countdown=5)


