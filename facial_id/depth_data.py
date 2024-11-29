from deepface import DeepFace
from deepface.modules.verification import __extract_faces_and_embeddings

def verification(img1_p, img2_p):

  result = DeepFace.verify(
    img1_path = img1_p,
    img2_path = img2_p,
  )

  print(result["verified"])

verification("registration_capture.jpg", "verification_capture.jpg")


def facial_embeddings(img):
  embedd = __extract_faces_and_embeddings(img)
  print(embedd)

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