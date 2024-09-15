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
    resized_img = cv2.resize(img, (640, 480))

    imgoffset = (bg_width - img_width) // 2
    y_offset = (bg_height - img_height) // 2_height, img_width, _ = resized_img.shape
    x_

    imgBackground[y_offset:y_offset + img_height,
                  x_offs] = resized_img

    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)
