<p align="center">
  <img src="demo/deepface-style-badge.png" width="120" />
  <br />
  <strong>#1 Trending Capstone Project</strong> &nbsp;|&nbsp; Blockchain + Facial Biometric &nbsp;|&nbsp; Built with ❤️
  <br />
  <a href="https://img.shields.io/github/stars/yourusername/secure-face-access?style=flat-square">⭐ Stars</a> &nbsp;
  <a href="https://img.shields.io/github/forks/yourusername/secure-face-access?style=flat-square">🔗 Forks</a> &nbsp;
  <a href="https://img.shields.io/github/issues/yourusername/secure-face-access?style=flat-square">🛠️ Issues</a> &nbsp;
  <a href="https://img.shields.io/github/license/yourusername/secure-face-access?style=flat-square">📝 License: MIT</a> &nbsp;
  <a href="https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square">✅ Tests Passing</a> &nbsp;
  <a href="https://img.shields.io/badge/docker-ready-blue?style=flat-square">🐳 Docker Ready</a> &nbsp;
  <a href="https://img.shields.io/badge/firebase-integrated-yellow?style=flat-square">🔥 Firebase Integrated</a> &nbsp;
  <a href="https://img.shields.io/badge/Capstone-2025-purple?style=flat-square">🎓 Capstone 2025</a> &nbsp;
  <a href="https://img.shields.io/badge/Built_with-Hyperledger_Fabric-blueviolet?style=flat-square">⛓️ Built with Hyperledger</a> &nbsp;
</p>

---

# 🔐 Secure Face Access

Secure Face Access is a full-stack access control system that leverages **facial biometric authentication**, **blockchain-based logging**, and **role-based access approvals** to enable dynamic, secure access in large institutions and organizations.

In large institutions like universities or corporations, access control needs to be **dynamic and decentralized**. For example, imagine a student needing access to a restricted lab. Traditionally, this would involve IT or security personnel, which can lead to delays. But what if a professor could approve access instantly, directly from their dashboard?

That’s the problem **Secure Face Access** solves. By combining facial recognition, blockchain-backed logs, and a permission-based access workflow, we enable **seamless, secure access**—without unnecessary bottlenecks or middlemen.

Built with **Hyperledger Fabric**, **Python**, **React**, and **Firebase**, this system allows users to register and authenticate using facial recognition, submit access requests to authorized personnel (e.g., professors), and view access logs stored immutably on the blockchain.

---

![Secure Face Access Demo](demo/demo.gif)  
*Example: Live login using facial verification and blockchain-backed access approval.*

---

## 🚀 Features

- 🔍 **Facial Biometric Login** – Powered by FaceNet512 and liveness detection using a canonical model.
- ⛓️ **Blockchain Integration** – Access requests and logs stored immutably using Hyperledger Fabric.
- 👩‍🏫 **Role-Based Approvals** – Professors or admins can approve access requests in real-time.
- 📜 **Access Logs Dashboard** – Users can view audit trails, access history, and security metadata.
- 🔐 **Passwordless Authentication** – Fast, secure, and intuitive user experience.

---

## 🛠️ Tech Stack

- **Frontend**: React, Firebase Auth
- **Backend**: Python (Flask), DeepFace, OpenCV, MediaPipe
- **Blockchain**: Hyperledger Fabric, CouchDB, Chaincode (Go)
- **Tools**: Docker, Bash

---

## 📦 Installation

### ✅ Clone the Repository

```bash
git clone https://github.com/SRshohan/secure-face-access.git
cd secure-face-access
```

---

### 🔧 Backend Setup (Python + Blockchain)

**Install Python dependencies:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Install and configure Hyperledger Fabric:**
Install Fabric binaries and configure the network First
```bash
cd fabric
./network.sh up
./network.sh createChannel
```

> 🔐 You must have Docker and Fabric binaries installed. See [Hyperledger Fabric Docs](https://hyperledger-fabric.readthedocs.io/) for setup.

**Run the Flask API server:**

```bash
cd ../backend
python app.py
```

---

### 💻 Frontend Setup (React + Firebase)

```bash
cd face-fabric-access
npm install
npm start
```

> Make sure to configure your Firebase project in `firebaseConfig.js`.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- **Sohanur Rahman** – Project Lead, Backend & Blockchain
- **[Sohanur Rahman], [Olga Diyamandoglu]** – Frontend & UI Design
- **[Dr. Mahmoud Amin]** – Capstone Supervisor

---

## 📬 Contact

For any inquiries or collaboration opportunities, please email: `srahman06@manhattan.edu`

---

## 📈 Future Improvements

See future roadmap for planned features like:

- Multi-modal biometrics
- Mobile integration
- Edge deployment for IoT

