import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
counter = 0

#try:
#	GPIO.wait_for_edge(17, GPIO.FALLING)
#	counter += 1
#	print(counter)
#except KeyboardInterrupt:
#	GPIO.cleanup()
#GPIO.cleanup()

def eventbla():
	print("PULSE")

GPIO.add_event_detect(17,callback=eventbla, bouncetime=100)
GPIO.cleanup()


