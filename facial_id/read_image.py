import cv2 
import time
from deepface import DeepFace


def take_picture_with_countdown(title, delay=7, output_path="captured_image.jpg"):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    start_time = time.time()
    while time.time() - start_time < delay:
        ret, frame = cap.read()
        if ret:
            # Display the countdown on the frame
            remaining_time = int(delay - (time.time() - start_time))
            cv2.putText(frame, f"Taking picture in {remaining_time}s, smile.", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f"Camera Feed {title}", frame)

        # Break if user presses ESC
        if cv2.waitKey(1) & 0xFF == 27:
            print("Cancelled by user.")
            cap.release()
            cv2.destroyAllWindows()
            return

    # Capture and save the final frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"Picture saved as {output_path}")
    else:
        print("Error: Failed to capture the image.")

    cap.release()
    cv2.destroyAllWindows()

take_picture_with_countdown(title="verification", output_path="verification_capture.jpg")