# 👁️‍🗨️ Face Recognition with Real-Time Firebase Database

This project is a **Python-based face recognition attendance system** that uses a webcam to recognize faces and updates student data in **Firebase Realtime Database and Storage** in real time.

---

## 📸 Features

- Real-time face recognition using `face_recognition` and `OpenCV`
- Firebase Realtime Database for student data and attendance logging
- Firebase Storage for storing and retrieving student images
- Stylish overlays with `cvzone` for improved UI/UX
- Automatically updates total attendance and last seen timestamp
- Displays student details and image on successful recognition

---

## 📂 Folder Structure
```bash
project/
├── Resources/
│   ├── background.jpg # UI background
│   ├── pk.json # Firebase Admin SDK key
│   └── mode/ # Mode images for different UI states
├── EncodeFile.p # Pickle file containing known encodings and IDs
├── main.py # Main face recognition script
├── requirements.txt
└── README.md
```

---

## 🔧 Requirements

### ✅ Python Version
- Python **3.7 - 3.10** (Recommended: 3.8 or 3.9)

### ✅ Python Packages
Install all with:
```bash
pip install -r requirements.txt
```

### ✅ System Requirements
Webcam

C++ build tools for compiling dlib

Windows:
Install Visual Studio Build Tools with:

MSVC v14.x

Windows 10 SDK

C++ build tools

Ubuntu/Linux:
```bash
sudo apt update
sudo apt install build-essential cmake python3-dev
```
##🔥 Firebase Setup

Create a project on Firebase Console

Enable Realtime Database and Storage

Go to Project Settings → Service Accounts → Generate new private key

Place the .json key in Resources/pk.json

Structure for your Firebase:


```bash


Students/
  student_id/
    name: "John Doe"
    major: "CS"
    standing: "Good"
    year: "3rd"
    starting_year: "2021"
    total_attendance: 5
    last_attendance: "2024-07-11 13:30:45"
```

##🚀 How to Run

```bash
python main.py
```
Show your face to the webcam

On successful match:

Your student data will appear on screen

Attendance will be updated in Firebase

## 📌 Notes
Make sure EncodeFile.p is already created using known images and encodings

Set Firebase rules to allow authenticated read/write or test with open rules

Image paths in Firebase Storage should match Images/{studentId}.png

## 📷 Demo
Coming Soon – GIF or video of the interface in action.

## 👨‍💻 Author
Syed Farman Ali





