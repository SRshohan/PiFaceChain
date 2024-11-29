from multiprocessing import Process
from face_mesh import draw_landmarks_on_camera
from deepface import DeepFace
import os

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def biometric(img1_p, img2_p):
    result = DeepFace.verify(
        img1_path=img1_p,
        img2_path=img2_p,
    )
    print(result["verified"])

if __name__ == "__main__":
    # Process 1: Run MediaPipe
    p1 = Process(target=draw_landmarks_on_camera, kwargs={"output_path": "test_3.jpg"})
    p1.start()
    p1.join()  # Wait for the process to complete

    # Process 2: Run DeepFace
    p2 = Process(target=biometric, args=("registration_capture.jpg", "test_3.jpg"))
    p2.start()
    p2.join()

