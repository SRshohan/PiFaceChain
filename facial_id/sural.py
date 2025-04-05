from deepface import DeepFace
import cv2
import os
import time
from command import InvokeFunction


def biometric(img1, img2_path):
    # If img1 is a numpy array (frame from camera)
    # we need to save it temporarily to use with DeepFace
    if not isinstance(img1, str):
        temp_path = "temp_frame.jpg"
        cv2.imwrite(temp_path, img1)
        img1_path = temp_path
    else:
        img1_path = img1
    
    try:
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
        )
        print(f"Verification result: {result['verified']}")
        return result["verified"]
    except Exception as e:
        print(f"Error in verification: {e}")
        return False
    finally:
        # Clean up the temporary file if we created one
        if not isinstance(img1, str) and os.path.exists("temp_frame.jpg"):
            os.remove("temp_frame.jpg")



if __name__ == "__main__":
    from helper import decode_base64_to_image
    from command import QueryFromBlockchain
    import json
    import base64

    ot = QueryFromBlockchain("ReadProfile", ["0002"])
    if ot["success"]:
        print("Query successful:", ot["output"], "It worked!!")
        # Decode the base64 string to an image
        data = json.loads(ot["output"])
        decoded_image = decode_base64_to_image(data["fe"], "decoded_image.jpg")
        if decoded_image is not None:
            print("Image successfully decoded and saved as decoded_image.jpg")
            # cv2.imshow("Decoded Image", decoded_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    else:
        print("Query failed:", ot["error"])
    
    cap = cv2.VideoCapture(0)
    reference_img = "None_face_cropped.jpg"  # Make sure this file exists
    
    # Check if reference image exists
    if not os.path.isfile(reference_img):
        print(f"Error: Reference image '{reference_img}' not found!")
        exit(1)
    
    print("Starting camera capture. Press 'q' to quit...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame
        cv2.imshow("Camera", frame)
        
        # Save current frame temporarily
        temp_frame = "current_frame.jpg"
        cv2.imwrite(temp_frame, frame)
        time.sleep(5)
        
        # Check verification every few frames (not every frame to avoid performance issues)
        try:
            result = biometric(temp_frame, decoded_image)
            if result:
                print("Match found!")
                break
        except Exception as e:
            print(f"Verification error: {e}")
        
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists(temp_frame):
        os.remove(temp_frame)
        
    print("Process completed!")






