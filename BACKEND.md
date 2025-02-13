# Backend System Architecture

## 1. Core Microservices

### A. Facial Recognition Service
**Purpose:**  
Process live camera feeds and match captured faces with stored user profiles.

**Key Components:**  
- **Model Training & Inference:** Use a facial recognition model (e.g., FaceNet, ArcFace, or DeepFace) integrated with NVIDIA TensorRT and DeepStream on the Jetson Nano.

**API Endpoint:**  
- **POST /recognize**  
  **Input:** Video frame or image.  
  **Output:** Matched user profile (ID, name, facial embedding, etc.) if available.

**Workflow:**  
1. Preprocess the input frame (using CUDA for speed).
2. Run inference on the facial recognition model.
3. Compare embeddings against the stored profiles.
4. Return a match along with a confidence score.

### B. User Management & Profile Service
**Purpose:**  
Manage user registrations, store facial images/embeddings, and maintain friend relationships.

**Database:**  
- **Choice:** PostgreSQL or MongoDB.

**Key API Endpoints:**  
- **POST /users/register**  
  Register a new user along with their facial image.  
- **GET /users/:id**  
  Retrieve a user profile, including their facial-ID details and friend list.  
- **PUT /users/:id**  
  Update user profile information (e.g., add or remove friends).

### C. Incident/Event Management Service
**Purpose:**  
Detect, log, and process events (accidents, intrusions, violence) based on input from the facial recognition service.

**Key API Endpoints:**  
- **POST /incidents**  
  Log a new incident (including timestamp, location, detected event type, and affected user ID).  
- **GET /incidents**  
  Retrieve a list of past incidents.

**Integration:**  
- **Facial Recognition Integration:** When an incident is detected, the recognition service provides the victim’s ID.  
- **Blockchain Integration:** Calls the Blockchain Service to store a tamper-proof log of the event.

### D. Notification Service
**Purpose:**  
Automatically notify relevant users (e.g., victim’s friends) as well as campus security/police when a high-severity incident occurs.

**Key API Endpoint:**  
- **POST /notify**  
  **Input:** Notification payload (user IDs, incident description, location).  
  **Output:** Confirmation of notification dispatch.

**Tech Stack:**  
Integrate with messaging services like Firebase Cloud Messaging, Twilio (SMS), or email APIs.

### E. Blockchain Service (Hyperledger Fabric)
**Purpose:**  
Securely record incident metadata on a tamper-proof, permissioned ledger.

**Key Components:**  
- **Smart Contracts (Chaincode):** Define how incidents are logged.  
- **Dedicated Channels:**  
  - **General Channel:** Stores regular incident logs.  
  - **Police Channel:** A restricted channel for high-severity events (e.g., violence) that automatically notifies law enforcement.

**Key API Endpoints:**  
- **POST /blockchain/log**  
  Log incident data (timestamp, location, incident type, and brief description).  
- **GET /blockchain/log/:id**  
  Retrieve a log entry for audit purposes.

## 2. Data Flow & Integration

**Live Feed Ingestion:**  
Cameras send video frames to the Facial Recognition Service.

**Identification:**  
The service processes the frame and identifies known users by matching facial embeddings.

**Event Triggering:**  
If an incident is detected (e.g., a victim falls), the Incident Management Service is called, passing along the recognized user’s ID and event metadata.

**Blockchain Logging:**  
The event details are stored immutably via the Blockchain Service.

**Notification:**  
The Notification Service retrieves the victim’s profile from the User Management Service (including friend list) and sends out alerts along with location data.

**Dedicated Channels:**  
For high-severity events, the service publishes messages to a dedicated police channel with restricted access.