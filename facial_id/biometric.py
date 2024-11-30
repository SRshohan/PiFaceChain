from deepface import DeepFace
from deepface.modules.verification import __extract_faces_and_embeddings

def biometric(img1_p, img2_p):

  result = DeepFace.verify(
    img1_path = img1_p,
    img2_path = img2_p,
  )

  print(result["verified"])

biometric("registration_capture.jpg", "image.png")


def facial_embeddings(img1, img2):
  embedd1 = __extract_faces_and_embeddings(img1)
  embedd2 = __extract_faces_and_embeddings(img2)
  return embedd1, embedd2

# facial_embeddings("captured_image.jpg")

# embedding_objs = DeepFace.represent(
#   img_path = "picture.jpg"
# )

# embedding_objs1 = DeepFace.represent(
#   img_path = "picture1.JPG"
# )

# print(embedding_objs)
# print("\nSeparate\n")

# print(embedding_objs1)