#aman = 0-15 , normal=16-27 , bahaya 28-40
    
def fstatus (s,x,y):
    
    #x=16 y=27
    if (s > x and s <= y):
        hasil = 2
        return hasil
        #return normal
    elif (s > y):
        hasil = 3
        return hasil
        #return Bahaya
    elif (s < x):
        hasil = 1
        return hasil
        #print ("Aman")
        #return Aman
   
    