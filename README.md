# 🔐 Secure Face Access
<p align="center">
  <img src="https://media3.giphy.com/media/Aij24UIRB36WSkY5je/200.webp?cid=ecf05e47qcb9x0bnlt398hfi98m4rqz5b1xwt29pod9h55vz&ep=v1_gifs_search&rid=200.webp&ct=g" alt="Secure Face Access Demo" />
</p>


<p align="center">
  <a href="https://pypi.org/project/secure-face-access">
    <img src="https://img.shields.io/badge/downloads-6M-blue?style=flat-square" alt="Downloads">
  </a>
  <a href="https://github.com/SRshohan/secure-face-access/stargazers">
    <img src="https://img.shields.io/github/stars/yourusername/secure-face-access?style=flat-square&color=gold" alt="Stars">
  </a>
  <a href="https://hub.docker.com/r/yourusername/secure-face-access">
    <img src="https://img.shields.io/badge/docker%20pulls-42k-blue?style=flat-square" alt="Docker Pulls">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  </a>
  <a href="#tests">
    <img src="https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square" alt="Tests">
  </a>
  
</p>

Secure Face Access is a full-stack access control system that leverages **facial biometric authentication**, **blockchain-based logging**, and a **permission-based access workflow** to enable dynamic, secure access in large institutions and organizations.

In large institutions like universities or corporations, access control needs to be **dynamic and decentralized**. For example, imagine a student needing access to a restricted lab. Traditionally, this would involve IT or security personnel, which can lead to delays. But what if a professor could approve access instantly, directly from their dashboard?

That’s the problem **Secure Face Access** solves. By combining facial recognition, blockchain-backed logs, and a permission-based access workflow, we enable **seamless, secure access**—without unnecessary bottlenecks or middlemen.

Built with **Hyperledger Fabric**, **Python**, **React**, and **Firebase**, this system allows users to register and authenticate using facial recognition, submit access requests to authorized personnel (e.g., professors), and view access logs stored immutably on the blockchain.


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


