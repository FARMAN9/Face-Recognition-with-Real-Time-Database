import cv2
import os

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load the background and overlay images
imgBackground = cv2.imread('Resources/background.jpg')
if imgBackground is None:
    raise FileNotFoundError("Background image not found.")

imgBackground = cv2.resize(imgBackground, (1080, 720))

# Load mode images from the folder
folderModePath = 'Resources/mode'
modePathList = os.listdir(folderModePath)

imgModeList = []
for path in modePathList:
    img_path = os.path.join(folderModePath, path)
    img = cv2.imread(img_path)
    if img is not None:
        imgModeList.append(img)
    else:
        print(f"Failed to load image from {img_path}")

print(f"Loaded {len(imgModeList)} mode images.")

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image from camera.")
        break

    # Resize the camera capture to fit the region in the background
    h = 400
    w = 400
    resized_img = cv2.resize(img, (w, h))

    # Ensure the target region is within the bounds of imgBackground
    if imgBackground.shape[0] >= 50 + h and imgBackground.shape[1] >= 10 + w:
        imgBackground[50:50 + h, 10:10 + w] = resized_img
    else:
        print("Target region for camera image exceeds background bounds.")

    # Overlay mode image if it exists
    if len(imgModeList) > 1:
        mode_img = imgModeList[1]
        mode_h, mode_w = mode_img.shape[:2]
        target_h = 648
        target_w = 438

        # Resize mode image if necessary
        if mode_h != target_h or mode_w != target_w:
            mode_img = cv2.resize(mode_img, (target_w, target_h))

        # Ensure the target region is within the bounds of imgBackground
        if imgBackground.shape[0] >= 50 + target_h and imgBackground.shape[1] >= 808 + target_w:
            imgBackground[50:50 + target_h, 808:808 + target_w] = mode_img
        else:
            print("Target region for mode image exceeds background bounds.")
    else:
        print("Not enough mode images loaded.")

    # Show the combined image
    cv2.imshow('Face Attendance', imgBackground)

    # Wait for 1 ms and check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
