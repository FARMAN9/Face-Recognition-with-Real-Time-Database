import cv2
import os
from PIL import Image
import numpy as np




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



file= 

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

    # Wait for 1 ms and check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
