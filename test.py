import RPi.GPIO as GPIO
from time import strftime,sleep,time
from sys import argv

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# Suppress "channel already in use" warning
GPIO.setwarnings(False)

wait = 0.03
try:
	wait = float(argv[1])
except:
	pass

def main(wait):
	
	counter = 0
	total = 0
	while True:
        	input_value = GPIO.input(17)
		if (input_value == 0):
			counter += 1
			print "======================== PULSE " + str(counter)
			total += 1
			#return(total)
			pulse=open("/home/pi/elec/pulse.dat","w")
			pulse.write(strftime("%H:%M:%S") + "," + str(1))
			pulse.close()
		else:
			counter = 0
			#print "-"
	        #print "Input Value (PIN 17):", input_value
	        sleep(wait)

if __name__ == '__main__':
	main(wait)
