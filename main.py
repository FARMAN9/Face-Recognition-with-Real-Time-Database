import cv2
import numpy as np
import pickle
import face_recognition
import cvzone
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db, storage

# Firebase Initialization
cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattrealtime-9f69c.appspot.com"
})
bucket = storage.bucket()

# Load static assets
imgBackground = cv2.imread('Resources/background.jpg')
imgBackground = cv2.resize(imgBackground, (1080, 720))
imgModeList = [
    cv2.resize(cv2.imread(f'Resources/mode/{f}'), (438, 648))
    for f in os.listdir('Resources/mode')
]

# Load encoded data
with open('EncodeFile.p', 'rb') as f:
    encodeListKnown, studentIds = pickle.load(f)

executor = ThreadPoolExecutor()

# Firebase Utilities
async def fetch_student_info(student_id):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: db.reference(f'Students/{student_id}').get())

async def update_attendance(student_id, student_info):
    loop = asyncio.get_event_loop()
    def _update():
        ref = db.reference(f'Students/{student_id}')
        ref.child('total_attendance').set(student_info['total_attendance'])
        ref.child('last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    await loop.run_in_executor(executor, _update)

async def fetch_student_image(student_id):
    loop = asyncio.get_event_loop()
    def _get_image():
        blob = bucket.get_blob(f'Images/{student_id}.png')
        if blob:
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            return cv2.imdecode(array, cv2.IMREAD_COLOR)
        return np.zeros((216, 171, 3), dtype=np.uint8)
    return await loop.run_in_executor(executor, _get_image)

async def recognize_faces(rgb_small_frame):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: (
        face_recognition.face_locations(rgb_small_frame),
        face_recognition.face_encodings(rgb_small_frame)
    ))

# Main Loop
async def main_loop():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    modeType = 0
    counter = 0
    id = -1
    studentInfo = {}
    imgStudent = []
    frame_count = 0
    frame_skip = 3

    while True:
        success, img = cap.read()
        if not success:
            break

        imgBackground[162:162 + 480, 55:55 + 640] = img
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        faceLocs, encodesCurFrame = [], []
        if frame_count % frame_skip == 0:
            faceLocs, encodesCurFrame = await recognize_faces(rgb_small_frame)
        frame_count += 1

        id = -1  # Reset ID every frame unless matched

        for encodeFace, faceLoc in zip(encodesCurFrame, faceLocs):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            distances = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(distances)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                center_x = x1 + (x2 - x1) // 2 + 55
                center_y = y1 + (y2 - y1) // 2 + 162
                radius = max(x2 - x1, y2 - y1) // 2 + 10
                cv2.circle(imgBackground, (center_x, center_y), radius, (0, 255, 0), 4)

                if counter == 0:
                    counter = 1
                    modeType = 1
                    studentInfo = await fetch_student_info(id)
                    imgStudent = await fetch_student_image(id)

        if counter != 0:
            if 10 < counter < 20:
                modeType = 2

            if counter <= 10 and studentInfo:
                cv2.putText(imgBackground, f"{studentInfo['name']}", (500, 100),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                cv2.putText(imgBackground, f"Attendance: {studentInfo['total_attendance']}", (500, 140),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 100, 0), 1)
                cv2.putText(imgBackground, f"Standing: {studentInfo['standing']}", (500, 180),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)
                cv2.putText(imgBackground, f"Year: {studentInfo['year']} | Start: {studentInfo['starting_year']}", (500, 220),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)
                cv2.putText(imgBackground, f"Major: {studentInfo['major']}", (500, 260),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1)

                if imgStudent is not None:
                    resizedImgStudent = cv2.resize(imgStudent, (171, 216))
                    imgBackground[175:391, 909:1080] = resizedImgStudent

            counter += 1

            if counter == 10 and studentInfo:
                last_time = datetime.strptime(studentInfo['last_attendance'], "%Y-%m-%d %H:%M:%S")
                elapsed = (datetime.now() - last_time).total_seconds()
                if elapsed > 40:
                    studentInfo['total_attendance'] += 1
                    await update_attendance(id, studentInfo)

            if counter >= 20:
                counter = 0
                modeType = 0
                studentInfo = {}
                imgStudent = []

        # Display mode image
        if modeType < len(imgModeList):
            imgBackground[50:698, 500:938] = imgModeList[modeType]

        # === ✅ Custom Status Message ===
        if id != -1:
            if counter <= 10:
                msg = "Face Recognized"
                color = (0, 255, 0)
            elif counter < 20:
                msg = "Updating Attendance..."
                color = (0, 165, 255)
            else:
                msg = "Welcome!"
                color = (255, 255, 255)
        else:
            msg = "Looking for Face..."
            color = (0, 0, 255)

        cv2.putText(imgBackground, msg, (350, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        # Show frame
        cv2.imshow("Face Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the async loop
if __name__ == '__main__':
    asyncio.run(main_loop())
