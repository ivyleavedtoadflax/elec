#!/usr/bin/python

import RPi.GPIO as GPIO
#from time import sleep
from time import strftime,sleep,time
from socket import gethostname
import string, os, sys, sqlite3, psycopg2, server_cred

######################### Setup GPIO PINS #########################

# Use Broadcom chip reference for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Name pins

pin4 = 17       # Photoresistor 

GPIO.setup(pin4, GPIO.IN)

# Define functions

def getLight():
	input_value = GPIO.input(pin4)
	sleep(0.03)
	if (input_value == 0):
		return(0.001)
	else:
		return(0)

# Run data recording LED init sequence

def ledFlash(i,j):	
	ledCount = 0
	while ledCount < i:
		GPIO.output(pin2, GPIO.HIGH)
		sleep(j)
		GPIO.output(pin2, GPIO.LOW)
		sleep(j)
		ledCount +=1

def write_log_csv(ts,day,night,val):
        log = open("/home/pi/elec/Log.csv", "a")
	log.write("\n" + str(ts) + "," + str(day) + "," + str(night) + "," + str(val))
	log.close()	

def write_log_psql(ts,day,night,val):

        conn_string = str("dbname = '"+ server_cred.db_name + "' user = '" + server_cred.username + "' host = '" + server_cred.host_ip + "' password = '" + server_cred.password + "'")
        conn = psycopg2.connect(conn_string)
        curs = conn.cursor()
        query_string = str("INSERT INTO elec values('" + str(ts) + "','" + str(day) + "','" + str(night) + "','" + str(val) + "');")
        curs.execute(query_string)
        conn.commit()
        curs.close()
        conn.close()

def main():

        initial = open("/home/pi/elec/initial.vals","r")
        day = float(initial.readline())
        night = float(initial.readline())
        initial.close()

	while True:
		timeout = time() + 60
	
		counter = 0
		while timeout > time():
			counter += getLight()

                timestamp = strftime("%Y-%m-%d %H:%M:%S")
		
		if int(strftime("%H")) in range(7,22):
			day += counter
		else:
			night += counter
		
		try:
			write_log_psql(timestamp,day,night,counter)
		except:
			pass

		try:
			write_log_csv(timestamp,day,night,counter)
		except:
			pass
	
        	initial = open("/home/pi/elec/initial.vals","w")
        	initial.write(str(day) + "\n" + str(night))
        	initial.close()

if __name__ == '__main__':
	main()

GPIO.cleanup()
