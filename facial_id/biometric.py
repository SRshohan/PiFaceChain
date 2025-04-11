import json
import subprocess
from deepface import DeepFace
import sys

def biometric(img1_p, img2_p):
    result = DeepFace.verify(
        img1_path=img1_p,
        img2_path=img2_p,
    )
    print(result["verified"])

def facial_embeddings(img1):
    import tensorflow as tf
    tf.keras.backend.clear_session()
    from deepface.modules.verification import __extract_faces_and_embeddings
    embedd1 = __extract_faces_and_embeddings(img1)
    return embedd1


from webui_register import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


file_name = "form_data.json"


# Open the file in read mode to load existing data
try:
    with open(file_name, "r") as file:
        existing_data = json.load(file)
        if not existing_data:
            raise ValueError(f"The file {file_name} is empty or invalid.")
except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
    print(f"Error reading {file_name}: {e}")
    existing_data = []
campus_id = existing_data[-1]["Campus ID"]
name = existing_data[-1]["Name"]
email = existing_data[-1]["Email"]
department = existing_data[-1]["Department"]
# fe = existing_data[-1]["fe"]
# Update the data
existing_data[-1]["fe"] = str(facial_embeddings(f"{campus_id}_registered_face.jpg"))

# Save back the updated data to the file
with open(file_name, "w") as file:
    json.dump(existing_data, file, indent=4)


def updateStateDB(campus_id, name, email, department, fe):
    # Construct the JSON argument directly as a list
    args_list = ["CreateProfile", str(campus_id), name, email, department, fe]
    
    # Convert the list into JSON format expected by the chaincode
    args_json = json.dumps({"Args": args_list})

    # Prepare the shell script with the updated command
    script = f'''
    cd hf/fabric-samples/test-network
    export PATH=${{PWD}}/../bin:$PATH
    export FABRIC_CFG_PATH=${{PWD}}/../config/

    # Set the environment variables for the peer CLI
    export CORE_PEER_TLS_ENABLED=true
    export CORE_PEER_LOCALMSPID="Org1MSP"
    export CORE_PEER_TLS_ROOTCERT_FILE=${{PWD}}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
    export CORE_PEER_MSPCONFIGPATH=${{PWD}}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
    export CORE_PEER_ADDRESS=localhost:7051

    peer chaincode invoke \\
    -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \\
    --tls --cafile "${{PWD}}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \\
    --peerAddresses $CORE_PEER_ADDRESS \\
    --tlsRootCertFiles $CORE_PEER_TLS_ROOTCERT_FILE \\
    -C mychannel -n ledger \\
    -c '{args_json}'
    '''

    # Build the command using bash or zsh based on your system configuration
    command = ["bash", "-c", script]

    # Execute the command and return the result
    return subprocess.run(command, text=True, capture_output=True)

fe = existing_data[-1]["fe"]
# Run the updateStateDB function
result = updateStateDB(campus_id, name, email, department, fe)

# Output the result
print(result.stdout)
if result.stderr:
    print(f"Error: {result.stderr}")






# from deepface import DeepFace
# from deepface.modules.verification import __extract_faces_and_embeddings
# import sys
# import json
# import subprocess


# def biometric(img1_p, img2_p):

#   result = DeepFace.verify(
#     img1_path = img1_p,
#     img2_path = img2_p,
#   )

#   print(result["verified"])

# # biometric("registration_capture.jpg", "image.png")


# def facial_embeddings(img1):
#   embedd1 = __extract_faces_and_embeddings(img1)
#   return embedd1[0][0]

# file_name = "form_data.json"

# # Open the file in read mode to load existing data
# with open(file_name, "r") as file:
#     existing_data = json.load(file)

# # Update the data
# existing_data[0]["fe"] = facial_embeddings("0123_registered_face.jpg")

# # Save back the updated data to the file
# with open(file_name, "w") as file:
#     json.dump(existing_data, file, indent=4)

# campus_id = existing_data[0]["Campus ID"]
# name = existing_data[0]["Name"]
# email = existing_data[0]["Email"]
# department = existing_data[0]["Department"]
# fe = existing_data[0]["fe"]

# def updateStateDB(campus_id, name, email, department, fe):
#    script = f"""
#             cd hf/fabric-samples/test-network && peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n ledger -c '{"Args":["CreateProfile","{campus_id}","{name}","{email}","{department}","{fe}"]}'

#             """
#    return subprocess.run(["zsh", script], text=True, capture_output=True)


# updateStateDB(campus_id, name, email, department, fe)

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