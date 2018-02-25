
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import atexit

import pigpio
pi = pigpio.pi("192.168.0.10")
#daftar kartu
kartu1 = '134215103172'
kartu2 = '214245103'
kartu3 = '24011017386'
#continue_reading = True


def rfid():
	start = True
	while start== True:
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
			 if UIDcode == (kartu1 or kartu2 or kartu3):
				print "kartuku terdetek"
				koneksi()				
				start =False
				
		else:
			print "Unrecognised Card"

def b():
	counter =0
	while counter < 1:
		pi.set_servo_pulsewidth(4,500)
		time.sleep(0.5)
		pi.set_servo_pulsewidth(4,2000)
		time.sleep(0.5)		
		counter=counter+1
		pi.set_servo_pulsewidth(4,0)

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print "Connected To Broker"
		global Connected
		Connected = True
		tampung = True
	else:
		print "Connection Failed"

def on_message(client, userdata, message):
	print "Message received:" + message.payload
	simpan = message.payload.decode(encoding='UTF-8')	
	if simpan == "disp":
			print "dispensed"			
			b()	
			on_message
	elif simpan == "end":
		print "ended"
		#pi.stop()
		client.disconnect()
		rfid()
		
	else:
		print "nothing"
	
		
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def koneksi():
	alamatbroker="18.194.47.96"
	client= mqtt.Client("P2")
	client.on_connect= on_connect
	client.on_message= on_message
	client.connect(alamatbroker)
#client.loop_start()
	client.subscribe("cia/coba")	
	client.loop_forever()
#Connected = False

#baca rfid
signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()
rfid()


atexit.register(GPIO.cleanup)


