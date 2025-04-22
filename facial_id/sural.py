from deepface import DeepFace
import cv2
import os
import time
from helper import decode_base64_to_image
from command import QueryFromBlockchain, InvokeFunction, InvokeOnBlockchain
import json
from hybrid_approach import track_eyes_with_liveness
from helper import encode_image_to_base64, decode_base64_to_image
import requests
import re

def extract_payload(stderr_output):
    if not isinstance(stderr_output, str):
        print("Input is not a string:", type(stderr_output))
        return None

    #  Find the payload string using regex
    match = re.search(r'payload:"((?:\\.|[^"\\])*)"', stderr_output)
    if not match:
        print("No payload found in stderr.")
        return None

    # Extract and clean escaped characters
    payload_str = match.group(1)

    # Unescape backslashes (decode \" into ")
    try:
        # Safely unescape escaped sequences like \", \n, etc.
        unescaped_str = bytes(payload_str, "utf-8").decode("unicode_escape")
        return json.loads(unescaped_str)
    except Exception as e:
        print("Failed to parse JSON:", e)
        return None

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

def register_no_camera(campus_id):
    # 🧠 Capture face via webcam
    frame = track_eyes_with_liveness()
    base64_face = encode_image_to_base64(frame)
    ot = QueryFromBlockchain("ReadProfile", [campus_id])
    if ot["success"]:
        print("Query successful:", ot["output"], "It worked!!")
        # Decode the base64 string to an image
        user = json.loads(ot["output"])
        
        parameters = [
                user["campusID"], user["name"], user["email"], user["department"], base64_face
            ]
        result = InvokeOnBlockchain("UpdateProfile", parameters)
        print("Invoke successful:", result["output"], "It worked!!")
 
    else:
        print("Query failed:", ot["error"])


def registration_process(campus_id, name, email, department):
    # Capture the image using the hybrid approach.
    captured_img = track_eyes_with_liveness()
    
    # Encode the captured image to base64.
    base64_string = encode_image_to_base64(captured_img)
    
    # Build parameters for the chaincode function call.
    parameters = [campus_id, name, email, department, base64_string]
    function = "CreateProfile"
    response = InvokeFunction(function, parameters)
    if response["success"]:
        print("Invoke successful:", response["output"], "It worked!!")
    else:
        print("Invoke failed:", response["error"])

def verification(campus_id):
    ot = QueryFromBlockchain("ReadProfile", [campus_id])
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
    # reference_img = "None_face_cropped.jpg"  # Make sure this file exists
    
    # # Check if reference image exists
    # if not os.path.isfile(reference_img):
    #     print(f"Error: Reference image '{reference_img}' not found!")
    #     exit(1)
    
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
        
        
        # Check verification every few frames (not every frame to avoid performance issues)
        try:
            result = biometric(temp_frame, decoded_image)
            if result:
                response = requests.get(f"http://149.61.245.217:5000/open")
                logdata = InvokeOnBlockchain("VerifyProfile",[campus_id, "Granted"])
                print("Match found!", result, logdata) # Removed response
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
    return extract_payload(logdata.get("stderr"))

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import json
from flask_mail import Mail, Message

class UserLogs(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('campusID')
        if not email:
            return jsonify({'error': 'No email provided'})

        try:
            response = InvokeOnBlockchain("ReadProfile", [email])
            if not response["success"]:
                return jsonify({'error': response.get("error", "Blockchain invocation failed")})

            # Extract payload from stderr
            payload = extract_payload(response.get("stderr", ""))
            if not payload:
                return jsonify({'error': 'Failed to parse payload from blockchain response'})

            return jsonify({
                'message': 'User logs retrieved successfully',
                'logs': payload
            })

        except Exception as e:
            return jsonify({'error': str(e)})



# This a camera endpoint for registration (not used & failed to open camera) OLD
# class Register(Resource):
#     def post(self):
#         data = request.get_json()
#         campus_id = data.get('campusID')
#         name = data.get('name')
#         email = data.get('email')
#         department = data.get('department')
#         if not campus_id or not name or not email or not department:
#             return jsonify({'error': 'Incomplete data provided'})
#         # register user
#         try:
#             # registration_process(campus_id, name, email, department, "None_face_cropped.jpg")
#             register_no_camera(campus_id, name, email, department, "None_face_cropped.jpg") 
#             return jsonify({'message': 'User registered successfully'})
#         except Exception as e:
#             return jsonify({'error': str(e)})

class Register(Resource):
    def post(self):
        data = request.get_json()
        campus_id = data.get('campusID')
        name = data.get('name')
        email = data.get('email')
        department = data.get('department')

        if not campus_id or not name or not email or not department:
            return jsonify({'error': 'Incomplete data provided'})

        try:
            # Just store profile with empty face
            result = InvokeOnBlockchain("CreateProfile", [email, name, email, department, "placeholder_fe"])
            if not result["success"]:
                return jsonify({'error': 'Blockchain registration failed'})

            return jsonify({
                'message': 'User registered successfully',
                'capture_url': f'/register/capture/{campus_id}'
            })
        except Exception as e:
            return jsonify({'error': str(e)})


class ApproveAccess(Resource):
    def get(self, tx_id):
        result = InvokeOnBlockchain("ApproveAccessRequest", [tx_id, "Approved"])

        # ✅ First try extracting from stderr
        payload = extract_payload(result.get("stderr", ""))

        # 🔁 If not found in stderr, fallback to output (stdout)
        if payload is None:
            try:
                payload = json.loads(result["output"])
            except Exception as e:
                print("Fallback JSON parse failed:", e)

        print("Payload:", payload)

        if payload is not None:
            return f"<h2>✅ Access request {tx_id} approved successfully!</h2>"
        else:
            return f"<h2>❌ Failed to approve request: {result.get('error', 'Unknown error')}</h2>", 400

class DenyAccess(Resource):
    def get(self, tx_id):
        result = InvokeOnBlockchain("ApproveAccessRequest", [tx_id, "Denied"])
        payload = extract_payload(result.get("stderr", ""))
        if payload is None:
            try:
                payload = json.loads(result["output"])
            except Exception as e:
                print("Fallback JSON parse failed:", e)

        print("Payload:", payload)

        if payload is not None:
            return f"<h2>✅ Access request {tx_id} denied successfully!</h2>"
        else:
            return f"<h2>❌ Failed to approve request: {result.get('error', 'Unknown error')}</h2>", 400

if __name__ == "__main__":
    userInput = input("Enter 1 for registration or 2 for verification: ")
    if userInput == "1":
        # registration_process("srahman06@manhattan.edu", "sr", "srahman", "ece")  # Replace with actual values (campus_id, name, email, department)
        register_no_camera("srshohan02@gmail.com")
    elif userInput == "2":
        verification("srshohan02@gmail.com")
    else:
        print("Invalid option selected.")
    # app = Flask(__name__)
    # CORS(app)
    # api = Api(app)

    # # 🔐 Flask-Mail Config
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = 'mugleeisback@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'vvlnhiibmqlycyrb'
    # app.config['MAIL_DEFAULT_SENDER'] = 'mugleeisback@gmail.com'
    # mail = Mail(app)

    # # Resources
    # api.add_resource(UserLogs, '/getUserLogs')
    # api.add_resource(Register, '/register')
    # api.add_resource(RegisterNoCam, '/registernocam')
    # api.add_resource(RequestAccess, '/requestAccess')
    # api.add_resource(ApproveAccess, '/approve/<string:tx_id>')
    # api.add_resource(DenyAccess, '/deny/<string:tx_id>')


    # app.run(debug=True, host='0.0.0.0', port=5001)


    