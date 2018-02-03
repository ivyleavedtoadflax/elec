#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from random import randint
from sys import argv

#	(ORANGE) 3.3v	[][]	5v (RED)
#	I2C0 SDA	[][]	DO NOT CONNECT
#	I2C0 SCL	[][]	GROUND (BLACK)
#	(GREEN) GPIO 4	[][]	UART TXD
#	DO NOT CONNECT	[][]	UART RXD
#	(YELLOW) GPIO 17[][]	GPIO 18 (ORANGE)
#	(BLUE) GPIO 21	[][]	DO NOT CONNECT
#	(PURPLE) GPIO 22[][]	GPIO 23
#	DO NOT CONNECT	[][]	GPIO 24
#	SPI MOSI	[][]	DO NOT CONNECT
#	SPI MISO	[][]	GPIO 25
#	SPI SCLK	[][]	SP10 CEO N
#	DO NOT CONNECT	[][]	SP10 CE1 N

######################### Setup GPIO PINS #########################

# Use Broadcom chip reference for GPIO
GPIO.setmode(GPIO.BCM)

# Suppress "channel already in use" warning
GPIO.setwarnings(False)

# name pins

pin2 = 4       # LED

# Setup outputs
GPIO.setup(pin2, GPIO.OUT)
# GPIO.setup(pin5, GPIO.IN)

# Set initial pin states. Wired led on pin2 the wrong way so start high and go low!

def ledFlash(i,j,k):
        ledCount = 0
        while ledCount < i:
                GPIO.output(pin2, GPIO.HIGH)
                sleep(j)
                GPIO.output(pin2, GPIO.LOW)
                sleep(randint(1,k))
                ledCount +=1

def main():
	ledFlash(float(argv[1]),float(argv[2]),float(argv[3]))


if __name__ == '__main__':
	main()
