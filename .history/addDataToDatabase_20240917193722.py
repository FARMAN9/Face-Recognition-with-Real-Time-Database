import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("Resources/pk.json")
firebase_admin.initialize_app(cred,{
  'databaseURL
})
