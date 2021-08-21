import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

dirmallist = db.reference('mallist/')
dmallist = dirmallist.get()
mal = dmallist['inmallist'].values()

wordCount = {} 

plus = 0
 
for word in mal:
 
    # Get 명령어를 통해, Dictionary에 Key가 없으면 0리턴
 
    wordCount[word] = wordCount.get(word, 0) + 1 
    
    keys = sorted(wordCount.keys())
 
for word in keys:
    if wordCount[word] > 1:
        print(word + ':' + str(wordCount[word])) 
        plus += (wordCount[word] - 1)

print(plus)