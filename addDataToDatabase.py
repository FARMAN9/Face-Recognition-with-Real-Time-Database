import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("Resources/pk.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/"
    })

# Reference to 'Students' node
ref = db.reference('Students')

# Student Data Dictionary
data = {
    "162226": {
        "name": "Alice Smith",
        "age": 18,
        "grade": 11,
        "major": "Mathematics",
        "starting_year": 2020,
        "total_attendance": 6,
        "year": 4,
        "standing": "G",
        "last_attendance": "2022-12-11 00:54:34"
    },
    "1622244": {
        "name": "xyz",
        "age": 18,
        "grade": 11,
        "major": "Mathematics",
        "starting_year": 2020,
        "total_attendance": 7,
        "year": 4,
        "standing": "G",
        "last_attendance": "2022-12-11 00:54:34"
    },
    "20240915": {
        "name": "xyz",
        "age": 18,
        "grade": 11,
        "major": "Mathematics",
        "starting_year": 2020,
        "total_attendance": 5,
        "year": 4,
        "standing": "G",
        "last_attendance": "2022-12-11 00:54:34"
    }
}

# Upload each student's data to Firebase
for key, value in data.items():
    ref.child(key).set(value)
    print(f"Uploaded student ID {key}")

