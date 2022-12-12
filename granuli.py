from machine import Pin,ADC
import utime
import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
from secrets import secrets
import socket

# uzstādīt vaslti, lai nerastos kļūdas
rp2.country('LV')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = secrets['ssid']
pw = secrets['pw']

wlan.connect(ssid, pw)

timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')                      #izvada informāciju par interneta pieslēgumu
    time.sleep(1)


laser = machine.Pin(5,Pin.OUT)
ldr = ADC(26)
time.sleep(5)
while True:
    laser.value(1)
    lightlevel = ldr.read_u16()
    print(lightlevel)
    if (lightlevel < 10000):                 #kad lāzers trāpa uz uztvērēju
        laser.value(0)
        print("No")
        utime.sleep(3)
        ifttt_url = 'https://maker.ifttt.com/trigger/pico_w_request(phone)/with/key/'+secrets['ifttt_key']        #pieslēdzās pie vietnes ar manu atslēgu un veic requestu, tālak atsūta uz telefonu ziņu
        request = requests.get(ifttt_url)
        print(request.content)
        request.close()
        time.sleep(300)
    else:
        print("Yes")
        laser.value(0)
        utime.sleep(200)
        laser.value(1)
        
        
