import cv2
import os
import time


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgBackground = cv2.imread('Resources/background.jpg')
loadImg = cv2.imread('Resources/scan.gif')
imgBackground = cv2.resize(imgBackground, (1920, 1080))
bg_height, bg_width, _ = imgBackground.shape
# import mode
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)
print(modePathList)

im

while True:
    success, img = cap.read()
    resized_img = cv2.resize(img, (640, 480))

    img_height, img_width, _ = resized_img.shape
    x_offset = (bg_width - img_width) // 2
    y_offset = (bg_height - img_height) // 2

    cv2.imshow('Face Attendance', imgBackground)
    imgBackground[y_offset:y_offset + img_height,
                  x_offset:x_offset + img_width] = resized_img

    cv2.imshow('Face Attendance', imgBackground)
    cv2.waitKey(1)
