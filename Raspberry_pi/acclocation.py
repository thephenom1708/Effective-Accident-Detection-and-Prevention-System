
import time
import serial
import string
import pynmea2
import RPi.GPIO as gpio
import requests
#to add the LCD library
"""import Adafruit_CharLCD as LCD"""
 
gpio.setmode(gpio.BCM)
""" 
#declaring LCD pins
lcd_rs = 17
lcd_en = 18
lcd_d4 = 27
lcd_d5 = 22
lcd_d6 = 23
lcd_d7 = 10
 
lcd_backlight = 2
 
lcd_columns = 16 #Lcd column
lcd_rows = 2 #number of LCD rows
 
lcd = LCD.Adafruit_CharLCD(lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
 """


port = "/dev/ttyAMA0"
API_ENDPOINT="http://192.168.43.59:8080/auth/api/sendLocation/"
# the serial port to which the pi is connected.
 
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
 
while 1:
    try:
        data = ser.readline()
    except:
        print("loading") 
#wait for the serial port to churn out data
 
    if data[0:6] == '$GPGGA': # the long and lat data are always contained in the GPGGA string of the NMEA data
 
        msg = pynmea2.parse(data)
 
#parse the latitude and print
        latval = msg.lat
        concatlat ="lat:" + str(latval)
        print(concatlat)
#lcd.set_cursor(0,0)
#lcd.message(concatlat)
 
#parse the longitude and print
        longval = msg.lon
        concatlong ="long:"+ str(longval)
        print(concatlong)
        #lcd.set_cursor(0,1)
        #lcd.message(concatlong)
        data={'latitude':concatlat,'longitude':concatlong}           
        time.sleep(0.5)#wait a little before picking the next data.
        break
    
r=requests.post(url=API_ENDPOINT,data=data)
print(r.content)
 
