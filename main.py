import RPi.GPIO as GPIO
import time

import sensor1
import sensor2
import servo as srv
import status
import json
import requests

srv.setup()

try :
    
    while True:
        
        ultra1 = sensor1.ping(5,6)
        ultra2 = sensor2.ping(24,23)
        
        #untuk mengukur ketinggian air
        #ults1 = pintu air / debit tumpah
        #ults2 = air masuk / sungai
        ults1 = 40 - ultra1
        ults2 = 40 - ultra2
        
        print "sensor 1", ults1
        print "sensor 2", ults2
        
        #hasil status 1,2,3 (Aman,Normal,Bahaya)
        stul1 =  status.fstatus(ults1,16,27)
        stul2 =  status.fstatus(ults2,16,27)
        
        
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
        #report = {'sungai' : utls2, 'debitumpha' : utls1}
        #inreport = requests.post('https://webibf.herokuapp.com/api/report/create', json=report)
        
    
    
except KeyboardInterrupt:
    print('Stop')
    srv.close()
    GPIO.cleanup()
