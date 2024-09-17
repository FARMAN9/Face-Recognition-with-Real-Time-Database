

import cv2
import os
from PIL import Image
import numpy as np
import pickle
import face_recognition
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load the background and overlay images
imgBackground = cv2.imread('Resources/background.jpg')
imgBackground = cv2.resize(imgBackground, (1080, 720))

# Initialize Firebase
cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattrealtime-9f69c.appspot.com"
})

bucket = storage.bucket()

# Load mode images from the folder
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)

imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(imgModeList)

# Load encoding data
with open('EncodeFile.p', 'rb') as file:
    encodeListKnowIDS = pickle.load(file)
encodeListKnown, studentIds = encodeListKnowIDS

print(studentIds)

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image from camera.")
        break

    h, w = 250, 250
    resized_img = cv2.resize(img, (h, w))

    # Overlay the resized image onto the background
    imgBackground[100:100 + h, 10:10 + w] = resized_img

    if modeType < len(imgModeList):
        modeImg = imgModeList[modeType]
        target_height, target_width = imgBackground[50:50 +
                                                    648, 500:500 + 438].shape[:2]

        # Resize modeImg to fit the target region
        resizedImgMode = cv2.resize(modeImg, (438, 648))
        imgBackground[50:50 + 648, 500:500 + 438] = resizedImgMode

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Changed COLOR_RGBA2RGB to COLOR_BGR2RGB
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

    for encodeface, faceloc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeface)
        distance = face_recognition.face_distance(encodeListKnown, encodeface)

        matchIndex = np.argmin(distance)

        if matches[matchIndex]:
            studentId = studentIds[matchIndex]
            y1, x2, y2, x1 = faceloc
            bbox = (10 + x1, 50 + y1, x2 - x1, y2 - y1)
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            id = studentIds[matchIndex]
            if counter == 0:
                cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                counter = 1
                modeType = 1

    if counter != 0:
        if counter == 1:
            # Get the Data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            if studentInfo:
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                if blob:
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)
                else:
                    imgStudent = np.zeros((216, 171, 3), dtype=np.uint8)

                # Update data of attendance
                datetimeObject = datetime.strptime(
                    studentInfo['last_attendance'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (
                    datetime.now() - datetimeObject).total_seconds()

                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(
                        studentInfo['total_attendance'])
                    ref.child('last_attendance').set(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    if modeType < len(imgModeList):
                        modeImg = imgModeList[modeType]
                        resizedImgMode = cv2.resize(modeImg, (438, 648))
                        imgBackground[50:50 + 648,
                                      500:500 + 438] = resizedImgMode

        if modeType != 3:
            if 10 < counter < 100:
                modeType = 2

            if modeType < len(imgModeList):
                modeImg = imgModeList[modeType]
                resizedImgMode = cv2.resize(modeImg, (414, 633))

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (500, 100),
                                cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(
                        studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    resizedImgStudent = cv2.resize(imgStudent, (171, 216))
                    imgBackground[175:175 + 216,
                                  909:909 + 171] = resizedImgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    if modeType < len(imgModeList):
                        modeImg = imgModeList[modeType]
                        resizedImgMode = cv2.resize(modeImg, (438, 648))
                        imgBackground[50:50 + 648,
                                      500:500 + 438] = resizedImgMode

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
