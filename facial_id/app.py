from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import json
from flask_mail import Mail, Message
from command import  InvokeOnBlockchain
from sural import Register, ApproveAccess, DenyAccess, UserLogs, extract_payload

class RequestAccess(Resource):
    def post(self):
        data = request.get_json()
        campus_id = data.get("campusID")
        location = data.get("location")
        from_time = data.get("fromTime")
        to_time = data.get("toTime")
        approval_email = data.get("approvalEmail")

        # Invoke blockchain
        response = InvokeOnBlockchain("RequestAccess", [campus_id, location, from_time, to_time, approval_email])
        if not response["success"]:
            return jsonify({"error": "Failed to invoke blockchain function"})
        payload = extract_payload(response.get("stderr", ""))
        if not payload:
            return jsonify({'error': 'Failed to parse payload from blockchain response'})
        try:
            tx_id = payload.get("txID")
            print("Transaction ID:", tx_id)
            request_id = payload.get("requestID")
        except Exception as e:
            return jsonify({'error': f'Failed to parse blockchain response: {str(e)}'})

        # ✅ Send approval email
        try:
            msg = Message(
                subject="New Access Request",
                recipients=[approval_email]
            )
            denyApproveUrl = "https://96da-2600-4041-5592-500-455f-ebb3-5f6-f03e.ngrok-free.app"

            msg.html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                .container {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    max-width: 600px;
                    margin: auto;
                    background-color: #f9f9f9;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                }}
                .header h2 {{
                    color: #333;
                    margin-bottom: 5px;
                }}
                .info {{
                    font-size: 16px;
                    line-height: 1.5;
                    margin-bottom: 30px;
                    color: #444;
                }}
                .label {{
                    font-weight: bold;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 10px 5px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    color: white;
                }}
                .approve {{
                    background-color: #28a745;
                }}
                .deny {{
                    background-color: #dc3545;
                }}
                .footer {{
                    margin-top: 30px;
                    font-size: 12px;
                    color: #888;
                    text-align: center;
                }}
                </style>
                </head>
                <body>
                <div class="container">
                <div class="header">
                    <h2>🔐 New Access Request</h2>
                </div>
                <div class="info">
                    <p><span class="label">User:</span> {campus_id}</p>
                    <p><span class="label">Location:</span> {location}</p>
                    <p><span class="label">Time Range:</span> {from_time} – {to_time}</p>
                    <p><span class="label">Transaction ID:</span> {tx_id}</p>
                </div>

                <div style="text-align: center;">
                    <a href="{denyApproveUrl}/approve/{tx_id}" class="button approve">✅ Approve Access</a>
                    <a href="{denyApproveUrl}/deny/{tx_id}" class="button deny">❌ Deny Access</a>
                </div>

                <div class="footer">
                    If you did not expect this request, please ignore this email.<br>
                    Powered by your Secure Access System 🚀
                </div>
                </div>
                </body>
                </html>
            """


            mail.send(msg)
            return jsonify({"message": "Request sent and email delivered.", "txID": tx_id})
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    # 🔐 Flask-Mail Config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'mugleeisback@gmail.com'
    app.config['MAIL_PASSWORD'] = 'vvlnhiibmqlycyrb'
    app.config['MAIL_DEFAULT_SENDER'] = 'mugleeisback@gmail.com'
    mail = Mail(app)

    # Resources
    api.add_resource(UserLogs, '/getUserLogs')
    api.add_resource(Register, '/register')
    # api.add_resource(RegisterNoCam, '/registernocam')
    api.add_resource(RequestAccess, '/requestAccess')
    api.add_resource(ApproveAccess, '/approve/<string:tx_id>')
    api.add_resource(DenyAccess, '/deny/<string:tx_id>')


    app.run(debug=True, host='0.0.0.0', port=5001)

# import os
# import cv2
# from command import InvokeFunction, QueryFromBlockchain
# from hybrid_approach import track_eyes_with_liveness
# from helper import encode_image_to_base64, decode_base64_to_image
# import json

# import requests
# from deepface import DeepFace
# import numpy as np

# os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# def biometric(img1, img2_path):
#     # If img1 is a numpy array (frame from camera)
#     # we need to save it temporarily to use with DeepFace
#     if not isinstance(img1, str):
#         temp_path = "temp_frame.jpg"
#         cv2.imwrite(temp_path, img1)
#         img1_path = temp_path
#     else:
#         img1_path = img1
    
#     try:
#         result = DeepFace.verify(
#             img1_path=img1_path,
#             img2_path=img2_path,
#         )
#         print(f"Verification result: {result['verified']}")
#         return result["verified"]
#     except Exception as e:
#         print(f"Error in verification: {e}")
#         return False
#     finally:
#         # Clean up the temporary file if we created one
#         if not isinstance(img1, str) and os.path.exists("temp_frame.jpg"):
#             os.remove("temp_frame.jpg")

# def registration_process(campus_id, name, email, department):
#     # Capture the image using the hybrid approach.
#     captured_img = track_eyes_with_liveness()
    
#     # Encode the captured image to base64.
#     base64_string = encode_image_to_base64(captured_img)
    
#     # Build parameters for the chaincode function call.
#     parameters = [campus_id, name, email, department, base64_string]
#     function = "CreateProfile"
#     response = InvokeFunction(function, parameters)
#     if response["success"]:
#         print("Invoke successful:", response["output"], "It worked!!")
#     else:
#         print("Invoke failed:", response["error"])


# def verification_process(campus_id):
#     # Query the blockchain for the registered profile using dynamic parameters.
#     ot = QueryFromBlockchain("ReadProfile", ["0002"])
#     if ot["success"]:
#         print("Query successful:", ot["output"], "It worked!!")
#         # Decode the base64 string to an image
#         data = json.loads(ot["output"])
#         decoded_image = decode_base64_to_image(data["fe"], "decoded_image.jpg")
#         if decoded_image is not None:
#             print("Image successfully decoded and saved as decoded_image.jpg")
#             # cv2.imshow("Decoded Image", decoded_image)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()
#     else:
#         print("Query failed:", ot["error"])
    
#     cap = cv2.VideoCapture(0)
#     # reference_img = "None_face_cropped.jpg"  # Make sure this file exists
    
#     # # Check if reference image exists
#     # if not os.path.isfile(reference_img):
#     #     print(f"Error: Reference image '{reference_img}' not found!")
#     #     exit(1)
    
#     print("Starting camera capture. Press 'q' to quit...")
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to grab frame")
#             break
        
#         # Display the frame
#         cv2.imshow("Camera", frame)
        
#         # Save current frame temporarily
#         temp_frame = "current_frame.jpg"
#         cv2.imwrite(temp_frame, frame)
        
        
#         # Check verification every few frames (not every frame to avoid performance issues)
#         try:
#             result = biometric(temp_frame, decoded_image)
#             if result:
#                 print("Match found!", result, type(result))
#                 break
#         except Exception as e:
#             print(f"Verification error: {e}")
        
#         # Break loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Clean up
#     cap.release()
#     cv2.destroyAllWindows()
#     if os.path.exists(temp_frame):
#         os.remove(temp_frame)
        
#     print("Process completed!")


# if __name__ == "__main__":
#     import threading

#     x = threading.Thread(target=verification_process("0002"))
#     x.start()
    
