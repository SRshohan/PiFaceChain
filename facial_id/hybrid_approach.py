import cv2
import mediapipe as mp
import math
import numpy as np

def calculate_ear(eye_points):
    """
    Calculate Eye Aspect Ratio (EAR) for blink detection.
    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    """
    # Vertical distances
    d1 = math.dist(eye_points[1], eye_points[5])
    d2 = math.dist(eye_points[2], eye_points[4])
    
    # Horizontal distance
    d3 = math.dist(eye_points[0], eye_points[3])
    
    return (d1 + d2) / (2 * d3)

def track_eyes_with_liveness():
    # Eye landmark indices for EAR calculation
    LEFT_EYE_EAR_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_EAR_INDICES = [362, 385, 387, 263, 380, 373]
    
    # Threshold values
    EAR_THRESHOLD = 0.25  # Below this = blink
    CONSECUTIVE_FRAMES = 2  # Number of frames for blink confirmation
    
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    cap = cv2.VideoCapture(0)
    
    # Liveness variables
    blink_counter = 0
    consecutive_blink_frames = 0
    liveness_confirmed = False
    
    # Flag to toggle between landmark view and regular view
    landmarks_active = True
    
    # Flag to indicate if a picture was taken
    picture_taken = False
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame from camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # Create a display frame - either with or without landmarks
        display_frame = frame.copy()
        # If landmarks are active, draw all face mesh points
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w = frame.shape[:2]
                
                # Get EAR calculation points
                left_eye_points = []
                right_eye_points = []
                
                # Left eye points for EAR
                for idx in LEFT_EYE_EAR_INDICES:
                    lm = face_landmarks.landmark[idx]
                    left_eye_points.append((lm.x * w, lm.y * h))
                    if landmarks_active:
                        cv2.circle(display_frame, (int(lm.x * w), int(lm.y * h)), 2, (0,255,0), -1)
                
                # Right eye points for EAR
                for idx in RIGHT_EYE_EAR_INDICES:
                    lm = face_landmarks.landmark[idx]
                    right_eye_points.append((lm.x * w, lm.y * h))
                    if landmarks_active:
                        cv2.circle(display_frame, (int(lm.x * w), int(lm.y * h)), 2, (0,255,0), -1)
            
                face_points = []
                if landmarks_active:
                    for landmark in face_landmarks.landmark:
                        x = int(landmark.x * w)
                        y = int(landmark.y * h)
                        face_points.append((x, y))
                        cv2.circle(display_frame, (x, y), 1, (0, 255, 0), -1)

                if face_points:
                    face_points = np.array(face_points)
                    padding = 30  # Pixels of padding around the face
                    x_min = max(0, np.min(face_points[:, 0]) - padding)
                    y_min = max(0, np.min(face_points[:, 1]) - padding)
                    x_max = min(w, np.max(face_points[:, 0]) + padding)
                    y_max = min(h, np.max(face_points[:, 1]) + padding)
                    
                    # Store the face bounding box
                    face_bbox = (int(x_min), int(y_min), int(x_max), int(y_max))
                    
                    # Draw bounding box on display frame
                    cv2.rectangle(display_frame, (face_bbox[0], face_bbox[1]), 
                                (face_bbox[2], face_bbox[3]), (0, 255, 255), 2)
                
                # Calculate EAR for both eyes
                left_ear = calculate_ear(left_eye_points)
                right_ear = calculate_ear(right_eye_points)
                avg_ear = (left_ear + right_ear) / 2.0
                
                # Detect blinks
                if avg_ear < EAR_THRESHOLD:
                    consecutive_blink_frames += 1
                else:
                    if consecutive_blink_frames >= CONSECUTIVE_FRAMES:
                        blink_counter += 1
                    consecutive_blink_frames = 0
                
                # Check liveness (require 3 blinks)
                if blink_counter >= 3 and not liveness_confirmed:
                    liveness_confirmed = True
                    print("Liveness confirmed! Real eyes detected.")

                # Draw status information
                cv2.putText(display_frame, f"EAR: {avg_ear:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(display_frame, f"Blinks: {blink_counter}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(display_frame, "Liveness: " + ("Confirmed" if liveness_confirmed else "Pending"), 
                            (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                            (0,255,0) if liveness_confirmed else (0,0,255), 2)

        # Instructions
        if liveness_confirmed and not picture_taken:
            cv2.putText(display_frame, "Press 'P' to take picture", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(display_frame, "Blink 3 times for liveness detection", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show landmark toggle instruction
        cv2.putText(display_frame, "Press 'L' to toggle landmarks", (50, 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Eye Liveness Detection", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('l') or key == ord('L'):
            landmarks_active = not landmarks_active
        elif key == ord('p') or key == ord('P'):
            if liveness_confirmed and face_bbox:
                # Crop the face from the original frame
                x_min, y_min, x_max, y_max = face_bbox
                face_crop = frame[y_min:y_max, x_min:x_max]
                
                # Save the cropped face
                cv2.imwrite("face_cropped.jpg", face_crop)
                picture_taken = True
                print("Cropped face saved as 'face_cropped.jpg'")
                
                # Display the cropped face for preview
                cv2.imshow("Cropped Face", face_crop)


    cap.release()
    cv2.destroyAllWindows()
    return liveness_confirmed

# Usage
if __name__ == "__main__":
    track_eyes_with_liveness()


    
    