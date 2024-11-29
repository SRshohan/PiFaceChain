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
    return result["verified"]

if __name__ == "__main__":
    question = input("Do you want to register(press 1) or login(press 2)? ")
    if question == "2":
        name = input("Please enter your name: ")
        # Process 1: Run MediaPipe
        p1 = Process(target=draw_landmarks_on_camera, kwargs={"output_path": f"verification/{name}.jpg", "task":"verification"})
        p1.start()
        p1.join()  # Wait for the process to complete

        # Process 2: Run DeepFace
        p2 = Process(target=biometric, args=(f"registration/{name}.jpg", f"verification/{name}.jpg"))
        p2.start()
        p2.join()
    else:
        name = input("Please enter your name: ")
        p3 = Process(target=draw_landmarks_on_camera, kwargs={"output_path": f"registration/{name}.jpg", "task":"Registration scan"})
        p3.start()
        p3.join()
