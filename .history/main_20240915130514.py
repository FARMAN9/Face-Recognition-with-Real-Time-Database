import cv2


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgBackground = cv2.imread('Resources/background.jpg')

while True:
    success, img = cap.read()
    resized_img = cv2.resize(img, (640, 480))
    imgBackground[162:162 + 480, 55:55 + 640] = re
    cv2.imshow('web cam', img)
    cv2.imshow('Face ATT', imgBackground)
    cv2.waitKey(1)
