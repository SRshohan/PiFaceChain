from multiprocessing import Process
from face_mesh import draw_landmarks_on_camera
from deepface import DeepFace
import os
from biometric import facial_embeddings
from deepface.modules.verification import __extract_faces_and_embeddings

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def biometric(img1_p, img2_p):
    result = DeepFace.verify(
        img1_path=img1_p,
        img2_path=img2_p,
    )
    print(result["verified"])
    return result["verified"]


if __name__ == "__main__":
    res = facial_embeddings("00234_registered_face.jpg")
    print(len(res))