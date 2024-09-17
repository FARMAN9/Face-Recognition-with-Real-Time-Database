import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')
data = {
    "162226": {
        "name": "Alice Smith",
        "age": 18,
        "grade": 11,
        "major": "Mathematics",
        "total_attendance": 6,
        "year": 4,
        "last_attendance": "2022-12-12 00:54:34"


    }

}


for key,value