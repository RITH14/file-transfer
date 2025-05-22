# 📁 Classic File Transfer: Real-Time File Transfer and Verification

## 📝 Overview

This project is a real-time file transfer system built using **TCP sockets** in a **client-server architecture**. It ensures data integrity through **file chunking** and **SHA256 checksum validation**, and includes basic support for **error detection and retransmission** in case of data corruption.

---

## 🚀 Features

- 📦 Reliable file transfer via TCP
- ✂️ File chunking with sequence numbers
- 🔐 SHA256 checksum verification
- 🧪 Simulated data corruption
- 🔁 Retransmission of corrupted chunks
- 📂 File reassembly and verification

---

## 🛠️ Architecture

### **Workflow**

1. **Client** sends a file to the **server**.
2. **Server**:
   - Saves the file
   - Splits it into 1024-byte chunks
   - Computes the SHA256 checksum
   - Sends chunk count and checksum to client
   - Sends chunks (with simulated corruption)
3. **Client**:
   - Receives and verifies chunks
   - Requests retransmission of corrupted chunks
   - Reassembles file and verifies checksum

---

## 📂 Project Structure

├── client.py # Client: Sends file, receives and verifies chunks
├── server.py # Server: Receives file, splits and sends chunks
├── README.md # Project documentation

---

## 🧰 Requirements

- Python 3.x
- Uses only standard Python libraries:
  - `socket`, `hashlib`, `pickle`, `os`, `random`, `threading`, `time`

---

## ⚙️ How to Use

### 1. Start the Server

```bash
python server.py
python client.py
