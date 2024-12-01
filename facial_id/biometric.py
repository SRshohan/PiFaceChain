from deepface import DeepFace
from deepface.modules.verification import __extract_faces_and_embeddings
import sys
import json
import subprocess


def biometric(img1_p, img2_p):

  result = DeepFace.verify(
    img1_path = img1_p,
    img2_path = img2_p,
  )

  print(result["verified"])

# biometric("registration_capture.jpg", "image.png")


def facial_embeddings(img1):
  embedd1 = __extract_faces_and_embeddings(img1)
  return embedd1[0][0]

file_name = "form_data.json"

# Open the file in read mode to load existing data
with open(file_name, "r") as file:
    existing_data = json.load(file)

# Update the data
existing_data[0]["fe"] = facial_embeddings("0123_registered_face.jpg")

# Save back the updated data to the file
with open(file_name, "w") as file:
    json.dump(existing_data, file, indent=4)


def updateStateDB():
   script =




# res = facial_embeddings("00234_registered_face.jpg")
# print(len(res))


# from webui_register import VideoCaptureThread, MainWindow

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     form_data = window.get_form_data()
#     window.show()
#     sys.exit(app.exec_())
#     res = facial_embeddings()


# embedding_objs = DeepFace.represent(
#   img_path = "picture.jpg"
# )

# embedding_objs1 = DeepFace.represent(
#   img_path = "picture1.JPG"
# )

# print(embedding_objs)
# print("\nSeparate\n")

# print(embedding_objs1)