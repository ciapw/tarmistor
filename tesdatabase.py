#---- RFID
import RPi.GPIO as GPIO
import MFRC522
import signal
#----
#--- clean gpio
import atexit
#---
import MySQLdb
db = MySQLdb.connect("localhost","tarmistor","tarmistorku","tarm")
cursor = db.cursor()
i = 0
b =str("coba%d" % i)

c = 10000

#--- procedures
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
			 #if UIDcode == kartu1 or UIDcode == kartu2 or UIDcode == kartu3:
			 print "kartuku terdetek"
			 global kodeku		
			 kodeku= UIDcode					
			 start =False
			 global i
			 i+=1
				
		else:
			print "Unrecognised Card"

	

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    
   
#---mau insert tag rfid cyn 134215103172
signal.signal(signal.SIGINT, end_read) 
MIFAREReader = MFRC522.MFRC522() 
rfid() 
#sql = """INSERT INTO user(id,name,saldo) 
	     #VALUES ("%s","%s","%s")""" % (kodeku,b,c)
#cursor.execute(sql) 
#db.commit() 
#print "SuccessFul adding" 
#------
	
#--- baca dari database
sql = """SELECT * FROM user 
	   WHERE id = '%s'""" % (kodeku)
cursor.execute(sql) 
results = cursor.fetchall()
for row in results:
		fid = row[0]
		fname = row[1]
		fsaldo = row[2]
		print ("fid=%s,fname=%s,fsaldo=%s") % (fid,fname,fsaldo)
#---

db.close()
atexit.register(GPIO.cleanup)
