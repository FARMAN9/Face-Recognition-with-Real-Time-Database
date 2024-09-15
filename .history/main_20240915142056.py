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
    imgModeList.append(os.path.join(folderModePath, path))

print(imgModeList)

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image from camera.")
        break

    # Resize the camera capture to fit the region in the background
    resized_img = cv2.resize(img, (272, 633))

    # Overlay the resized image onto the background
    imgBackground[22:22 + 633,404:4-08 + 272] = resized_img

    # Show the combined image
    cv2.imshow('Face Attendance', imgBackground)

    # Wait for 1 ms and check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
