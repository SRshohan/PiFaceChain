import base64
import cv2
import numpy as np
import os
from hybrid_approach import track_eyes_with_liveness

def decode_base64_to_image(base64_string, output_filename="decoded_image.jpg"):
    """
    Decode a base64 string back to a JPG image and save it
    
    Args:
        base64_string: The base64 encoded string representation of the image
        output_filename: The filename to save the decoded image to
    
    Returns:
        The decoded image as a NumPy array
    """
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        
        # Convert to numpy array
        np_array = np.frombuffer(image_data, np.uint8)
        
        # Decode the numpy array to an image
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        # Save the image
        cv2.imwrite(output_filename, image)
        
        print(f"Image successfully decoded and saved as {output_filename}")
        return image
    
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None
    
def encode_image_to_base64():
    """
    Capture an image using the hybrid approach and encode it to a base64 string
    
    Returns:
        The base64 encoded string representation of the captured image
    """

    captured_img = track_eyes_with_liveness()

    _, buffer = cv2.imencode('.jpg', captured_img)
    base64_string = base64.b64encode(buffer).decode('utf-8')
    return base64_string