import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattrealtime-9f69c-default-rtdb.firebaseio.com/"
})
ref = db.r
