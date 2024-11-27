from deepface import DeepFace

result = DeepFace.verify(
  img1_path = "picture.jpg",
  img2_path = "picture1.JPG",
)

# print(result)

embedding_objs = DeepFace.represent(
  img_path = "picture.jpg"
)

embedding_objs1 = DeepFace.represent(
  img_path = "picture1.JPG"
)

print(embedding_objs)
print("Separate\n")

print(embedding_objs1)