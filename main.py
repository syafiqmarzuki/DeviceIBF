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
import timeit
from datetime import datetime


start = timeit.default_timer()
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

saat_ini = datetime.now()
tgl = saat_ini.strftime('%d/%m/%Y') # format dd/mm/YY
jam = saat_ini.strftime('%H:%M:%S')

#fcm
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAa_ji2rI:APA91bFwwWcFsZaupSeZyZghKbN32x3Vp9QlKtHOpHfjY0Bo9Q1XeQTp_oN_c9NnUzsf3F3OpJ7oXsqsKQNbVBm4HXnwKwElhHPk2lBQ4h-Vjy_TljfCo1NKBZxukLGDeXPvHNt3JCks'
      }




# Create a tweet
    
while True:
    try:
        
        ultra1 = sensor1.ping(5,6)
        ultra2 = sensor2.ping(24,23)
       
        ults1 = 22 - ultra1
        ults2 = 37 - ultra2
        print(ults1);
        print(ults2);
        print('debit tumpah' , ults1);
        print('sungai' ,  ults2);
        
        fults1 = '{:.3}'.format(ults1)
        fults2 = '{:.3}'.format(ults2)
        
        stul1 =  status.fstatus(ults1,16,27)
        stul2 =  status.fstatus(ults2,16,27)
        
        
       # Create API object
        api = tweepy.API(auth)
        
        if (ults1 > 29):
            
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian sekarang pada Debit Tumpah sudah mencapai "+str(fults1)+" cm . Harap untuk bersiap siap menyelamatkan diri."
            api.update_status(pesan)
            print('post twitter debit')
            
        if (ults2 > 29):
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian sekarang pada Sungai sudah mencapai "+str(fults2)+" cm . Harap untuk bersiap siap menyelamatkan diri."
            api.update_status(pesan)
            print ('post twitter sungai')
        
        data = {
            "Raspi3/Sungai/":{
                "Ketinggian": fults2,
                "Status": stul2},
            "Raspi3/Debit": {
                "Ketinggian": fults1,
                "Status": stul1}
            }
        db.update(data)
            
        time.sleep(1)
        now = timeit.default_timer()
        if int(now - start) % 1800 == 0:
            report = {'sungai' : fults2, 'debittumpah' : fults1}
            inreport = requests.post('https://ibflood.herokuapp.com/api/report/create', json=report)
            print("berhasil post db")
        
        
        if (ults1 > 30 and ults2 > 30):
            
            body = {
                'notification': {
                    'title': 'Kondisi Bahaya',
                    'body': 'Harap Menyelamatkan Diri'},     
                'to':
                    '/topics/Notif-Bahaya',
                    'priority': 'high',
                'data': {
                    'sungai': fults1,
                    'debit': fults2 },
                    }
            response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
            print(response.status_code)
            print(response.json())
            notif_isi = "Harap untuk menyelamatkan diri anda karena situasi sudah bahaya ketinggian bendungan sudah mencapai" +(strfults1)+ "cm  dan sungai "+str(fults2)+ "cm ."
            notif = {'isi_notif' : notif_isi}
            inreport = requests.post('https://ibflood.herokuapp.com/api/notif/create', json=report)
            print("berhasil post notif")
            

                
        
        
        #print (fults1, stul1)
        #print (fults2, stul2)   
        
        
        #mengatur otomatis pintu servo
        if (ults1 > 25):
            #print ("Banjir Kiriman Buka")
            srv.ServoUp()
        elif (ults2 <= 25 ):
            #print ("Pintu Buka Terus")
            srv.ServoUp()
        elif (ults2 >= 25):
            #print ("Tutup Pintu")
            srv.ServoDown()
            
        

    except Exception as e:
        print('Duplicate tweet. Tidak Bisa post....')
        pass
        #srv.close()
        #GPIO.cleanup()
                
    
