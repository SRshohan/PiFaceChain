import os
import subprocess
import json
from hybrid_approach import track_eyes_with_liveness
import json 
import base64
import cv2

def InvokeFunction(function, parameters=None):
    # Ensure you're running from the expected directory structure.
    current_dir = os.getcwd()
    
    # Set the network directory relative to current_dir.
    network_directory = os.path.abspath(os.path.join(current_dir, "../hf/fabric-samples/test-network/"))
    # Define the bin directory relative to network_directory
    bin_directory = os.path.join(network_directory, "../bin")
    
    # Get the current PATH and add our directories.
    current_path = os.environ.get('PATH', '')
    new_path = f"{bin_directory}:{network_directory}:{current_path}"
    
    # Setup environment variables for the Fabric client.
    identity_variables = os.environ.copy()
    identity_variables.update({
        "PATH": new_path,
        "FABRIC_CFG_PATH": os.path.abspath(os.path.join(network_directory, "../config/")),
        "CORE_PEER_TLS_ENABLED": "true",
        "CORE_PEER_LOCALMSPID": "Org1MSP",
        "CORE_PEER_MSPCONFIGPATH": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp")
        ),
        "CORE_PEER_TLS_ROOTCERT_FILE": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
        ),
        "CORE_PEER_ADDRESS": "localhost:7051"
    })
    
    # Check if the peer binary exists.
    peer_path = os.path.join(bin_directory, "peer")
    if not os.path.exists(peer_path):
        return {"success": False, "error": f"Peer binary not found at {peer_path}"}
    
    # Prepare the arguments array
    args = [function]

    
    # If parameters is a string, add it as a single parameter
    if isinstance(parameters, str):
        args.append(parameters)
    # If parameters is a list/tuple, extend the args with it
    elif isinstance(parameters, (list, tuple)):
        args.extend(parameters)
    # If parameters is a dict, convert it to a JSON string
    elif isinstance(parameters, dict):
        args.append(json.dumps(parameters))
    
    # Construct the JSON arguments.
    json_args = json.dumps({"Args": args})
    
    print(f"Debug - JSON Args: {json_args}")  # Add debugging
    
    # Construct the chaincode query command.
    access = [
        peer_path,
        "chaincode", "invoke", 
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls", 
        "--cafile", os.path.abspath(
            os.path.join(network_directory, "organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem")
        ),
        "-C", "mychannel", 
        "-n", "ledger", 
        "--peerAddresses", "localhost:7051",
        "--tlsRootCertFiles", os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
        ),
        "-c", json_args
    ]
    
    try:
        print(f"Debug - Running command: {' '.join(access)}")  # debugging
        result = subprocess.run(access, cwd=network_directory, env=identity_variables, 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}
        
        print(f"Debug - Command output: {result.stdout.strip()}")  # debugging
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
# Function to query the blockchain for user data
def InvokeOnBlockchain(function, parameters=None):
    current_dir = os.getcwd()
    network_directory = os.path.abspath(os.path.join(current_dir, "../hf/fabric-samples/test-network/"))
    bin_directory = os.path.join(network_directory, "../bin")

    current_path = os.environ.get('PATH', '')
    new_path = f"{bin_directory}:{network_directory}:{current_path}"

    identity_variables = os.environ.copy()
    identity_variables.update({
        "PATH": new_path,
        "FABRIC_CFG_PATH": os.path.abspath(os.path.join(network_directory, "../config/")),
        "CORE_PEER_TLS_ENABLED": "true",
        "CORE_PEER_LOCALMSPID": "Org1MSP",
        "CORE_PEER_MSPCONFIGPATH": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp")
        ),
        "CORE_PEER_TLS_ROOTCERT_FILE": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
        ),
        "CORE_PEER_ADDRESS": "localhost:7051"
    })

    peer_path = os.path.join(bin_directory, "peer")
    if not os.path.exists(peer_path):
        return {"success": False, "error": f"Peer binary not found at {peer_path}"}

    # Handle parameters as before
    args = [function]
    if isinstance(parameters, str):
        args.append(parameters)
    elif isinstance(parameters, (list, tuple)):
        args.extend(parameters)
    elif isinstance(parameters, dict):
        args.append(json.dumps(parameters))
    
    json_args = json.dumps({"Args": args})

    # Full invoke command based on your reference
    access_device = [
        peer_path,
        "chaincode", "invoke",
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls",
        "--cafile", os.path.abspath(
            os.path.join(network_directory, "organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem")
        ),
        "-C", "mychannel",
        "-n", "ledger",
        "-c", json_args
    ]

    try:
        result = subprocess.run(access_device, cwd=network_directory, env=identity_variables, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}
        print(f"Debug - Command output: {result}")
        return {
            "success": True,
            "output": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }

    
    except Exception as e:
        return {"success": False, "error": str(e)}



def QueryFromBlockchain(function, parameters=None):
    # Ensure you're running from the expected directory structure.
    current_dir = os.getcwd()
    
    # Set the network directory relative to current_dir.
    network_directory = os.path.abspath(os.path.join(current_dir, "../hf/fabric-samples/test-network/"))
    # Define the bin directory relative to network_directory (bin is a sibling of test-network).
    bin_directory = os.path.join(network_directory, "../bin")
    
    # Get the current PATH and add our directories.
    current_path = os.environ.get('PATH', '')
    new_path = f"{bin_directory}:{network_directory}:{current_path}"
    
    # Setup environment variables for the Fabric client.
    identity_variables = os.environ.copy()
    identity_variables.update({
        "PATH": new_path,
        "FABRIC_CFG_PATH": os.path.abspath(os.path.join(network_directory, "../config/")),
        "CORE_PEER_TLS_ENABLED": "true",
        "CORE_PEER_LOCALMSPID": "Org1MSP",
        "CORE_PEER_MSPCONFIGPATH": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp")
        ),
        "CORE_PEER_TLS_ROOTCERT_FILE": os.path.abspath(
            os.path.join(network_directory, "organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt")
        ),
        "CORE_PEER_ADDRESS": "localhost:7051"
    })
    
    # Check if the peer binary exists.
    peer_path = os.path.join(bin_directory, "peer")
    if not os.path.exists(peer_path):
        return {"success": False, "error": f"Peer binary not found at {peer_path}"}
    
    peer_command = peer_path

    # Construct the JSON arguments.
    # This will produce a string like: {"Args":["ReadProfile","profile1"]}
    args = [function]
    # If parameters is a string, add it as a single parameter
    if isinstance(parameters, str):
        args.append(parameters)
    # If parameters is a list/tuple, extend the args with it
    elif isinstance(parameters, (list, tuple)):
        args.extend(parameters)
    # If parameters is a dict, convert it to a JSON string
    elif isinstance(parameters, dict):
        args.append(json.dumps(parameters))
    # Convert the arguments to JSON format
    json_args = json.dumps({"Args": args})
    
    # Construct the chaincode query command.
    access_device = [
        peer_command,
        "chaincode", "query", 
        "-C", "mychannel", 
        "-n", "ledger", 
        "-c", json_args
    ]
    
    try:
        result = subprocess.run(access_device, cwd=network_directory, env=identity_variables, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}
        
        print(f"Debug - Command output: {result.stdout}")
        return {"success": True, "output": result.stdout}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":

    import json
    import re

  

    def extract_payload(stderr_output):
        if not isinstance(stderr_output, str):
            print("Input is not a string:", type(stderr_output))
            return None

        # Step 1: Find the payload string using regex
        match = re.search(r'payload:"((?:\\.|[^"\\])*)"', stderr_output)
        if not match:
            print("No payload found in stderr.")
            return None

        # Step 2: Extract and clean escaped characters
        payload_str = match.group(1)

        # Step 3: Unescape backslashes (decode \" into ")
        try:
            # Safely unescape escaped sequences like \", \n, etc.
            unescaped_str = bytes(payload_str, "utf-8").decode("unicode_escape")
            return json.loads(unescaped_str)
        except Exception as e:
            print("Failed to parse JSON:", e)
            return None
        
    ot = InvokeOnBlockchain("ReadProfile", ["12340"])
    payload = extract_payload(ot.get("stderr"))

    print(json.dumps(payload, indent=2))
    print(type(payload))




    # Example usage with the correct parameters for your chaincode
    # function = "ReadProfile"
    # # Use the parameters that match your chaincode's expectations
    # parameters = ["00022"]
    
    # response = QueryFromBlockchain(function, parameters)
    
    # if response["success"]:
    #     print("Query successful:", response["output"], "It worked!!")
    #     data = json.loads(response["output"])
    #     print("Decoded data:", data["campusID"])
    # else:
    #     print("Query failed:", response["error"])



    # Example usage with the correct parameters for your chaincode
    # function = "CreateProfile"

    # captured_img = track_eyes_with_liveness()

    # _, buffer = cv2.imencode('.jpg', captured_img)
    # base64_string = base64.b64encode(buffer).decode('utf-8')
    
    # # Use the parameters that match your chaincode's expectations
    # parameters = ["0002", "Yash", "yash@y.com", "CSE", base64_string]

    # response = InvokeFunction(function, parameters)
    # if response["success"]:
    #     print("Invoke successful:", response["output"], "It worked!!")
    # else:
    #     print("Invoke failed:", response["error"])



    # from helper import decode_base64_to_image

    # ot = QueryFromBlockchain("ReadProfile", ["12340"])
    # if ot["success"]:
    #     print("Query successful:", ot["output"], "It worked!!")
    #     # Decode the base64 string to an image
    #     data = json.loads(ot["output"])
        
    #     decoded_image = decode_base64_to_image(data["fe"], "decoded_image.jpg")
    #     if decoded_image is not None:
    #         print("Image successfully decoded and saved as decoded_image.jpg")
    #         # cv2.imshow("Decoded Image", decoded_image)
    #         # cv2.waitKey(0)
    #         # cv2.destroyAllWindows()
    # else:
    #     print("Query failed:", ot["error"])

    