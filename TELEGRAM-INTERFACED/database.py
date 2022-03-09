import pyrebase


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initilaize_app():
    firebaseConfig = {"apiKey": "AIzaSyB90XbnKvjkFnEAXRKXwYUyOL92W04bFR0",
      "authDomain": "tast-telegran-bot.firebaseapp.com",
      "projectId": "tast-telegran-bot",
      "storageBucket": "tast-telegran-bot.appspot.com",
      "messagingSenderId": "663865393615",
      "appId": "1:663865393615:web:a456f154e39be804a792ba"}

    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase

def storage():
    firebase = initilaize_app()
    storage = firebase.storage()

def db_setup():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db

if __name__ == '__main__':
    storage()