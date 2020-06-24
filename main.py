import RPi.GPIO as GPIO
import time
import tweepy
import sensor1
import sensor2
import servo as srv
import status
import json
import requests
import pyrebase

import time

srv.setup()
#cfgfire.setup()
config = {
        "apiKey" : "AIzaSyBvtK_grzpMJFPd6HVhNVqLA9zf1xMYBGs",
        "authDomain" : "ibrebesf.firebaseapp.com",
        "databaseURL" : "https://ibrebesf.firebaseio.com/",
        "storageBucket" : "ibrebesf.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#twitter

auth = tweepy.OAuthHandler("8ZttJWOCRWYFc98DDBtK2K1xA", "f3z8UiSpqRklN2BkXubOd5yg6qZqZXC0zRugRALb8IWXEMpMrq")
auth.set_access_token("1253167579650158593-6c7cZ1o0bfIILvblMwy8rpR38O0UFK", "0fHrd7ILuK5iJWIMApr0NkFi4Rzkn6w7vpnmi27xI4YBz")

# Create a tweet
try :
    
    while True:
        
        ultra1 = sensor1.ping(5,6)
        ultra2 = sensor2.ping(24,23)
        
        #untuk mengukur ketinggian air
        #ults1 = pintu air / debit tumpah
        #ults2 = air masuk / sungai
        ults1 = 40 - ultra1
        ults2 = 40 - ultra2
        
        fults1 = '{:.3}'.format(ults1)
        fults2 = '{:.3}'.format(ults2)
        
        stul1 =  status.fstatus(ults1,16,27)
        stul2 =  status.fstatus(ults2,16,27)
        
        
       # Create API object
        api = tweepy.API(auth)
        
        if (ults1 > 29):
            pesan = "Ketinggian sekarang pada Debit Tumpah sudah mencapai "+str(fults1)+" cm . Harap untuk bersiap siap menyelamatkan diri."
            api.update_status(pesan)
            
        if (ults2 > 29):
            pesan2 = "Ketinggian sekarang pada Sungai sudah mencapai "+str(fults2)+" cm . Harap untuk bersiap siap menyelamatkan diri."
            api.update_status(pesan2)
        
        #update data firebase
        data = {
            "Raspi3/Sungai/":{
                "Ketinggian": fults2,
                "Status": stul2},
            "Raspi3/Debit": {
                "Ketinggian": fults1,
                "Status": stul1}
            }
        db.update(data)
        
        
        print (fults1, stul1)
        print (fults2, stul2)   
        
        
        #mengatur otomatis pintu servo
        if (ults1 > 25):
            print ("Banjir Kiriman Buka")
            srv.ServoUp()
        elif (ults2 <= 25 ):
            print ("Pintu Buka Terus")
            srv.ServoUp()
        elif (ults2 >= 25):
            print ("Tutup Pintu")
            srv.ServoDown()
            
        
        #update data sungai
        #sungai = {'ketinggian' : ults1 , 'status' : stul2}
        #upsungai = requests.put('https://webibf.herokuapp.com/api/sungai/1', sungai)
        
        #update data debittumpah
        #debittumpah = {'ketinggian' : ults2 , 'status' : stul1}
        #updebitt = requests.put('https://webibf.herokuapp.com/api/debittumpah/1', debittumpah)
            
        #insert report
        report = {'sungai' : ults2, 'debitumpah' : ults1}
        inreport = requests.post('https://webibf.herokuapp.com/api/report/create', json=report)
        print("berhasil")
        time.sleep(0.00009)
        
    
    
except KeyboardInterrupt:
    print('Stop')
    srv.close()
    GPIO.cleanup()
