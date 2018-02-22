#!/usr/bin/env python
# -*- coding: utf8 -*-
# Credit to mxgxw whose program this is based on

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import atexit
import pigpio

#led blink
GPIO.setmode(GPIO.BOARD) #harus ada utk setiap kali mau set GPIO)
GPIO.setup(11,GPIO.OUT) #set pin 11 sbg out

#setting servo putar rpi
#GPIO.setup(7,GPIO.OUT)
#p = GPIO.PWM(7,50)
#p.start(7.5)

#setting servo pigpio
pi = pigpio.pi("192.168.0.10")

#daftar kartu
kartuku = '134215103172'
continue_reading = True

def blink():
	GPIO.output(11,True)
	time.sleep(1)
	GPIO.output(11,False)
	time.sleep(1)
	GPIO.output(11,True)
	time.sleep(1)
	GPIO.output(11,False)
	time.sleep(1);
	
#def putar():
	#count= 0
	#while count <1:
		#p.ChangeDutyCycle(7.5)
		#time.sleep(1)
		#p.ChangeDutyCycle(12.5)
		#time.sleep(1)
		#p.ChangeDutyCycle(7.5)
		#time.sleep(1)
		#count = count +1;
def putarpig():
	counter = 0
	while counter < 1:
		pi.set_servo_pulsewidth(4,500)
		time.sleep(0.5)
		pi.set_servo_pulsewidth(4,2000)
		time.sleep(0.5)
		counter=counter+1
		pi.set_servo_pulsewidth(4,0)
		#pi.stop()

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
signal.signal(signal.SIGINT, end_read)


MIFAREReader = MFRC522.MFRC522()

while continue_reading:
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
# If a card is found
	if status == MIFAREReader.MI_OK:
		print "Card detected"

# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

# If we have the UID, continue
	if status == MIFAREReader.MI_OK:
		 # Print UID
		 UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
		 print UIDcode
		 if UIDcode == kartuku:
			print "kartuku terdetek"
			#blink()
			#putar()
			putarpig()
			
	else:
		print "Unrecognised Card"
            
atexit.register(GPIO.cleanup)
pi.stop()
