import cv2
import os

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load the background and overlay images
imgBackground = cv2.imread('Resources/background.jpg')
imgBackground = cv2.resize(imgBackground, (1080, 720))


# Load GIF or other resources (if needed)
loadImg = cv2.imread('Resources/scan.gif')

# Load mode images from the folder
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)

imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(imgModeList)

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image from camera.")
        break

    # Resize the camera capture to fit the region in the background
    h = 250
    w = 250
    resized_img = cv2.resize(img, (h, w))

    # Overlay the resized image onto the background
    imgBackground[50:50 + h, 10:10 + w] = resized_img

    imgBackground[50:50 + 648, 500:500 + 438] = imgModeList[0]

    # Show the combined image
    cv2.imshow('Face Attendance', imgBackground)
    cv2.imshow('gif',loadImg)

    # Wait for 1 ms and check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
