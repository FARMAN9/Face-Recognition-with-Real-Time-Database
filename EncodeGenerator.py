'''
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattrealtime-9f69c.appspot.com"
})


# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'  # sending data or images
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    print(blob)
    print(path)
    print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(images):
    encodeList = []
    for img in images:
        # Find face locations and encodings
        faceLocs = face_recognition.face_locations(img)
        encodings = face_recognition.face_encodings(img, faceLocs)

        if encodings:  # Check if any encodings were found
            encodeList.append(encodings[0])
        else:
            print("No face encodings found.")
    return encodeList


''' 
'''
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
    '''

'''
print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
'''

import cv2
import face_recognition
import pickle
import os
import asyncio
import firebase_admin
from firebase_admin import credentials, db, storage
from concurrent.futures import ThreadPoolExecutor

# Initialize Firebase
cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattrealtime-9f69c.appspot.com"
})
bucket = storage.bucket()

# Executor for threading
executor = ThreadPoolExecutor()

# Asynchronous function to upload image to Firebase Storage
async def upload_image_async(file_path, file_name):
    loop = asyncio.get_event_loop()
    def _upload():
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        return blob
    return await loop.run_in_executor(executor, _upload)

# Asynchronous face encoding
async def encode_face_async(image):
    loop = asyncio.get_event_loop()
    def _encode():
        faceLocs = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, faceLocs)
        return encodings[0] if encodings else None
    return await loop.run_in_executor(executor, _encode)

# Main async function
async def main():
    folderPath = 'Images'
    pathList = os.listdir(folderPath)
    print("Found images:", pathList)

    imgList = []
    studentIds = []
    tasks = []

    # Step 1: Load images, get IDs, and upload to Firebase
    for path in pathList:
        full_path = os.path.join(folderPath, path)
        img = cv2.imread(full_path)
        if img is not None:
            imgList.append(img)
            studentIds.append(os.path.splitext(path)[0])
            tasks.append(upload_image_async(full_path, f'{folderPath}/{path}'))
        else:
            print(f"Failed to load image: {path}")

    # Wait for all uploads to complete
    upload_results = await asyncio.gather(*tasks)
    for blob, path in zip(upload_results, pathList):
        print(f"Uploaded: {blob.public_url if blob else 'Failed'}")

    # Step 2: Encode faces asynchronously
    print("Encoding Started ...")
    encode_tasks = [encode_face_async(img) for img in imgList]
    encodeListKnown = await asyncio.gather(*encode_tasks)

    # Filter out None encodings
    encodeListFiltered = [enc for enc in encodeListKnown if enc is not None]
    studentIdsFiltered = [studentIds[i] for i, enc in enumerate(encodeListKnown) if enc is not None]

    print(f"Encoding complete: {len(encodeListFiltered)} faces encoded")

    # Step 3: Save encodings
    with open("EncodeFile.p", 'wb') as f:
        pickle.dump([encodeListFiltered, studentIdsFiltered], f)

    print("Encodings saved to EncodeFile.p")

# Run async main
if __name__ == "__main__":
    asyncio.run(main())
