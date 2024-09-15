import cv2
import os
import time


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgBackground = cv2.imread('Resources/background.jpg')
loadImg = cv2.imread('Resources/scan.gif')
imgBackground = cv2.resize(imgBackground, (1080, 720))

# import mode
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)
print(modePathList)

imgModeList = []

for path in modePathList:
    imgModeList.append(os.path.join(folderModePath, path))

print(imgModeList)


while True:
    success, img = cap.read()

    imgBackground[44:44 + 633, 808:808 + 414] = img

    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)
