import requests
import json
import sensor1
import sensor2
import status
import timeit
from datetime import datetime

start = timeit.default_timer()

saat_ini = datetime.now()
tgl = saat_ini.strftime('%d/%m/%Y') # format dd/mm/YY
jam = saat_ini.strftime('%H:%M:%S')



url = "https://api.wassenger.com/v1/messages"
url_get_phone = "https://ibflood.herokuapp.com/api/nohp"
response = requests.get(url = url_get_phone)
body = json.loads(str(response.text))
phone_numbers = body['data']
headers = {
    'content-type': "application/json",
    'token': "e634a1b525f85a007a6c49de61ccce530407c81c1f0b0f461789643ad00d33cede84ced7219c9354"
}


def convert_zero_to_plus_62(phone_number):
    if phone_number[0] == '0':
        string = phone_number[:0] + "+62" + phone_number[0+1:]
        new_phone_number = string
        return new_phone_number
    return phone_number

while True:
    try:
        ultra1 = sensor1.ping(5,6)
        ultra2 = sensor2.ping(23,24)
       
        ults1 = 38 - ultra1
        ults2 = 38 - ultra2
        fults1 = '{:.3}'.format(ults1)
        fults2 = '{:.3}'.format(ults2)
        stul1 =  status.fstatus(ults1,16,30)
        stul2 =  status.fstatus(ults2,13,25)
        
        if (ults1 > 34 and ults2 > 28):
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian air sekarang pada Bendungan sudah mencapai "+str(fults1)+" cm, dan sungai telah mencapai " +str(fults2) +" cm. Waspada akan adanya banjir, harap untuk para warga yang bermukim di area  dekat sungai pemali untuk  segera melakukan evakuasi dini. #simulasibanjir #tugasakhir"
            for i in range(len(phone_numbers)):
                phone = convert_zero_to_plus_62(phone_numbers[i]['no_hp'])

                payload = "{\"phone\":\""+phone+"\",\"message\":\""+pesan+"\"}"
                res = requests.post(url = url, data=payload, headers=headers)
            
            
        if (ults2 > 26):
            pesan = "Pada tanggal "+str(tgl)+" , jam "+str(jam)+" . Ketinggian sekarang pada Sungai sudah mencapai "+str(fults2)+" cm . Harap waspada air sungai akan meluap. Harap untuk para warga yang bermukim di dekat area sungai pemali untuk melakukan evakuasi dini. #simulasibanjir #tugaskhir"
            for i in range(len(phone_numbers)):
                phone = convert_zero_to_plus_62(phone_numbers[i]['no_hp'])

                payload = "{\"phone\":\""+phone+"\",\"message\":\""+pesan+"\"}"
                res = requests.post(url = url, data=payload, headers=headers)
                
    except Exception as e:
        #print('Duplicate tweet. Tidak Bisa post....')
        pass
        #srv.close()
        #GPIO.cleanup()
       



