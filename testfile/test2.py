import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

dirmallist = db.reference('mallist/')
dmallist = dirmallist.get()
count = list(dmallist['inmallist'].keys())
count = int(float(count[len(count) - 1])) + 1

print(count)