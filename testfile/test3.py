from discord import message
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#firebase
cred = credentials.Certificate("D:/Desktop/중요파일/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})


dirteamscno = db.reference('testteam/' + "지완/" + "1")
dirteamscno.update({"test":5520})

'''
list = dirteamscno.get()
print(list)
print(list['test'])
print(list.keys())
print(list.values())
dirteamscno.delete()
'''