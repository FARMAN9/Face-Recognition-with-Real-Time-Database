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


# Load GIF or other resources (if needed)
loadImg = 'Resources/scan.gif'


def display_gif(gif_path, delay=100):
    """
    Display an animated GIF using OpenCV.

    :param gif_path: Path to the GIF file.
    :param delay: Delay between frames in milliseconds (default is 100 ms).
    """
    # Load the GIF using Pillow
    gif = Image.open(gif_path)

    while True:
        # Display each frame of the GIF
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            gif.seek(0)  # Restart from the first frame

        # Convert the current frame to an OpenCV image
        frame = np.array(gif.convert('RGB'))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Show the current frame
        cv2.imshow('GIF Frame', frame)

        # Wait for a short period and check for 'q' key to exit
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# Load mode images from the folder
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)

imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(imgModeList)


file = open('EncodeFile.p', 'rb')
encodeListKnowIDS = pickle.load(file)
file.close()
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

    h = 250
    w = 250
    resized_img = cv2.resize(img, (h, w))

    # Overlay the resized image onto the background
    imgBackground[50:50 + h, 10:10 + w] = resized_img

    imgBackground[50:50 + 648, 500:500 +
                  438] = imgModeList[1]
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_RGBA2RGB)
    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)
    for encodeface, faceloc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeface)
        distance = face_recognition.face_distance(encodeListKnown, encodeface)
        print("Distance", distance)
        print('match', matches)

        # now we need min or lest value which matchs
        matchIndex = np.argmin(distance)
        print('index', matchIndex)

        if matches[matchIndex]:
            studentId = studentIds[matchIndex]
            print('Student ID:', studentId)
            y1, x2, y2, x1 = faceloc

            bbox = 10 + x1, 50 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(
                imgBackground, bbox, rt=0)

            id = studentIds[matchIndex]
            if counter == 0:
                cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                cv2.imshow("Face Attendance", imgBackground)
                cv2.waitKey(1)
                counter = 1
                modeType = 1
    if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (
                    datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(
                        studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 +
                        414] = imgModeList[modeType]
                    
                    
                    
        if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
    # Wait for 1 ms and check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
