# Frontend System Architecture

## 1. Web Dashboard (for Administrators & Security Personnel)

### Key Features & Pages:

#### Login / Authentication:
- Secure login with multi-factor authentication (MFA).
- Role-based access control (admin, security operator).

#### Dashboard Overview:
- **Incident Summary Widget:**
  - Total incidents, categorized by type (accidents, intrusions, violence).
- **Live Feed Grid:**
  - Real-time camera feeds with overlays showing detected faces and bounding boxes.
- **Notification Panel:**
  - Lists critical alerts (including events sent to the police channel).

#### User Management:
- **User Profiles:**
  - Detailed view of registered users, including facial-ID images, friend lists, and recent incident involvement.
- **Profile Editing:**
  - Interface for adding, updating, or removing user details and friend relationships.

#### Incident Log:
- **Filtering & Search:**
  - Filter incidents by time, type, or location.
- **Detailed View:**
  - Clicking on an incident shows details (timestamp, description, location, verified by blockchain).
- **Map Integration:**
  - Visualize incident locations using Google Maps or OpenStreetMap.

#### Blockchain Log Viewer:
- A dedicated page to view and verify blockchain logs with transaction IDs and timestamps.

#### Settings & Configurations:
- **Camera & Model Settings:**
  - Adjust parameters for facial recognition and incident detection.
- **Alert & Notification Settings:**
  - Configure who gets notified (e.g., friend list and security contacts) and how (SMS, email, push notifications).

### Tech Stack:
- **Framework:** React (or Angular/Vue)
- **UI Library:** Material-UI, Ant Design, or Bootstrap
- **Real-Time Updates:** WebSockets for live feed and notifications
- **Mapping:** Google Maps API or OpenStreetMap integration

## 2. Mobile Application (for Campus Users & Friends)

### Key Features:
- **User Profile & Facial-ID Display:**
  - Each user’s profile displays their facial-ID image along with basic personal info and a list of campus friends.
  - Ability to update profile details, including friend connections.

- **Incident Notifications:**
  - Real-time push notifications alerting users if one of their friends (or themselves) is involved in an incident.
  - Detailed alert view that shows the incident description, location on a map, and options to acknowledge or share the alert.

- **Incident Map:**
  - Interactive map showing recent incidents on campus.
  - Option to filter incidents by type or severity.

- **Live Feed (Optional):**
  - View select live feeds (if permitted) or stream snapshots from key areas.

### Tech Stack:
- **Framework:** React Native or Flutter
- **Notification Service:** Integration with Firebase Cloud Messaging (FCM) for push notifications
- **Maps:** Google Maps SDK for mobile or Mapbox

## 3. Integration Between Frontend and Backend

### RESTful APIs:
- All data (user profiles, incidents, notifications) are fetched using RESTful endpoints.

### Real-Time Communication:
- WebSockets (or Socket.IO) for live incident alerts and updates.

### Security:
- Secure communication over HTTPS.
- Role-based access control on API endpoints.

### User Session Management:
- JSON Web Tokens (JWT) or OAuth2 for managing user sessions and authorization.

## Example Workflow Scenario

### User Registration & Training:
- A new student registers via the mobile or web app, uploading their facial image.
- The system extracts facial embeddings and stores the profile (including a pre-defined friend list).

### Incident Occurrence:
- A camera detects an incident (e.g., a fall or violent event).
- The Facial Recognition Service processes the image, identifies the victim, and sends a match to the Incident Management Service.
- The incident is logged to the Blockchain Service.

### Notification Dispatch:
- The Notification Service retrieves the victim’s profile and friend list.
- Push notifications are sent out to the victim’s friends (e.g., “Alert: [Name] was detected at [Location] during an incident. Please check on them.”).

### Dashboard & Mobile App Updates:
- Administrators see the incident details, including blockchain verification, on the web dashboard.
- Friends receive push notifications on their mobile apps with incident details and a map view of the location.