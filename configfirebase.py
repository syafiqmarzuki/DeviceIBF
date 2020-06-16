import time
import json
#import requests
import pyrebase

def setup():
    config = {
        "apiKey" : "AIzaSyBvtK_grzpMJFPd6HVhNVqLA9zf1xMYBGs",
        "authDomain" : "ibrebesf.firebaseapp.com",
        "databaseURL" : "https://ibrebesf.firebaseio.com/",
        "storageBucket" : "ibrebesf.appspot.com"}
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.start_at
    
    
def close():
    db.stop()
if __name__ == '__main__':
    setup()
    
   
    
    