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
#srv.setup()
#cfgfire.setup()
config = {
        "apiKey" : "AIzaSyBvtK_grzpMJFPd6HVhNVqLA9zf1xMYBGs",
        "authDomain" : "ibflood.firebaseapp.com",
        "databaseURL" : "https://ibflood.firebaseio.com/",
        "storageBucket" : "ibflood.appspot.com"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# #twitter
# 
auth = tweepy.OAuthHandler("8ZttJWOCRWYFc98DDBtK2K1xA", "f3z8UiSpqRklN2BkXubOd5yg6qZqZXC0zRugRALb8IWXEMpMrq")
auth.set_access_token("1253167579650158593-6c7cZ1o0bfIILvblMwy8rpR38O0UFK", "0fHrd7ILuK5iJWIMApr0NkFi4Rzkn6w7vpnmi27xI4YBz")

saat_ini = datetime.now()
tgl = saat_ini.strftime('%d/%m/%Y') # format dd/mm/YY
jam = saat_ini.strftime('%H:%M')
url = "https://api.wassenger.com/v1/messages"
url_get_phone = "https://ibflood.herokuapp.com/api/nohp"
response = requests.get(url = url_get_phone)
body = json.loads(str(response.text))
phone_numbers = body['data']
now = timeit.default_timer()

# 
# #fcm
headerf = {
        'Content-Type': "application/json",
        'Authorization': "key=AAAAuHfdmTs:APA91bFCuAOeeCoOMfefqWLOkYvA62zakpdpcaEw-hgVHHufhL8RMGdf3-O3vBez-TAt5Wm9MTavJJoo-nWE17javt0zsaa72HD2HYUO4g7-PXPXud4xSgY_BEss4Mg624xLbP9J96de"
      }
headerwa = {
    'content-type': "application/json",
    'token': "e634a1b525f85a007a6c49de61ccce530407c81c1f0b0f461789643ad00d33cede84ced7219c9354"
}
# 
def convert_zero_to_plus_62(phone_number):
    if phone_number[0] == '0':
        string = phone_number[:0] + "+62" + phone_number[0+1:]
        new_phone_number = string
        return new_phone_number
    return phone_number



# Create a tweet
    
while True:
    try:
        
        ultra1 = sensor1.ping(5,6)
        ultra2 = sensor2.ping(23,24)
       
        ults1 = 38 - ultra1
        ults2 = 38 - ultra2

        
        fults1 = '{:.3}'.format(ults1)
        fults2 = '{:.3}'.format(ults2)
        
        fultss1 = '{:.0f}'.format(ults1)
        fultss2 = '{:.0f}'.format(ults2)
        
        stul1 =  status.fstatus(ults1,16,30)
        stul2 =  status.fstatus(ults2,13,25)
         
        
        data = {
            "Raspi3/Sungai/":{
                "Ketinggian": fults2,
                "Status": stul2},
            "Raspi3/Debit": {
                "Ketinggian": fults1,
                "Status": stul1}
            }
        db.update(data)
        
        
       # Create API object
        api = tweepy.API(auth)
        
        if (ults1 > 35 and ults2 > 26):
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian sekarang pada Debit Tumpah sudah mencapai "+str(fultss1)+" cm, dan sungai sudah mencapai " +str(fultss2) +" cm. Bahaya akan ada banjir datang, Harap untuk para warga menyelamatkan diri. #simulasibanjir #tugasakhir."
            #api.update_status(pesan)
            
            notif_isi = "Ketinggian sekarang pada Debit Tumpah sudah mencapai "+str(fultss1)+" cm, dan sungai sudah mencapai " +str(fultss2) +" cm. Bahaya akan ada banjir datang, Harap untuk para warga menyelamatkan diri. #simulasibanjir #tugasakhir."
            
            if             
#             for i in range(len(phone_numbers)):
#                 phone = convert_zero_to_plus_62(phone_numbers[i]['no_hp'])
# 
#                 payload = "{\"phone\":\""+phone+"\",\"message\":\""+pesan+"\"}"
#                 res = requests.post(url = url, data=payload, headers=headerwa)
#             #print('post twitter debit')
            time.sleep(1)
            if int(now - start) % 60 == 0:
                api.update_status(pesan)
                body = {
                    'notification': {
                    'title': 'Bahaya akan ada datang nya banjir.',
                    'body': notif_isi,
                    'sound' : 'default'},     
                    'to':
                    '/topics/Notif-Banjir',
                    'priority': 'high',
                    'data': {
                    'debit': fults1},
                    }
                response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headerf, data=json.dumps(body))
                print(response.status_code)
                print(response.json())
                notif = {'isi_notif' : notif_isi}
                inreport = requests.post('https://ibflood.herokuapp.com/api/notif/create', json=report)
                print("berhasil post notif")
                print("berhasil post twitter")
        elif (ults2 > 26):
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian sekarang pada Sungai sudah mencapai "+str(fultss2)+" cm . Waspada air sungai akan meluber. Harap bersiap yang rumah nya pinggiran sungai untuk menyelamatkan diri."            
            notif_isi = "Ketinggian sekarang pada Sungai sudah mencapai "+str(fultss2)+" cm . Waspada air sungai akan meluber. Harap bersiap yang rumah nya pinggiran sungai untuk menyelamatkan diri."
            #print ('post twitter sungai')
#             for i in range(len(phone_numbers)):
#                 phone = convert_zero_to_plus_62(phone_numbers[i]['no_hp'])
# 
#                 payload = "{\"phone\":\""+phone+"\",\"message\":\""+pesan+"\"}"
#                 res = requests.post(url = url, data=payload, headers=headerwa)
            if int(now - start) % 60 == 0:
                api.update_status(pesan)
                body = {
                    'notification': {
                    'title': 'Kondisi air Sungai akan meluap ke dataran tepi sungai.',
                    'body': notif_isi,
                    'sound' : 'default'},     
                    'to':
                    '/topics/Notif-Sungai',
                    'priority': 'high',
                    'data': {
                    'sungai': fults2 },
                    }
                response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headerf, data=json.dumps(body))
                print(response.status_code)
                print(response.json())
                notif = {'isi_notif' : notif_isi}
                inreport = requests.post('https://ibflood.herokuapp.com/api/notif/create', json=report)
                print("berhasil post notif")
            
                print("berhasil post twitter")


             
        time.sleep(1)
        #now = timeit.default_timer()
        if int(now - start) % 60 == 0:
            report = {'sungai' : fults2, 'debittumpah' : fults1}
            inreport = requests.post('https://ibflood.herokuapp.com/api/report/create', json=report)
            print("berhasil post db")

        
        
        
#         #mengatur otomatis pintu servo
#         if (ults1 > 25):
#             srv.ServoUp()
#         elif (ults2 <= 21):
#             srv.ServoUp()
#         elif (ults2 >= 20):
#             srv.ServoDown()
#      
        

    except Exception as e:
        print('Duplicate tweet. Tidak Bisa post....')
        pass
        #srv.close()
        #GPIO.cleanup()
                
    
