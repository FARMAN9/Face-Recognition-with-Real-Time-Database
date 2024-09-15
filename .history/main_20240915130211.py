import cv2


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgBackground = cv2.imread('Resources/background.jpg')

while True:
    success, img = cap.read()
    imgBackground[162]
    cv2.imshow('web cam', img)
    cv2.imshow('Face ATT', imgBackground)
    cv2.waitKey(1)
