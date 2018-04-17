'''
Test that LED blink detection works
'''

from time import strftime, sleep
from sys import argv
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# Suppress "channel already in use" warning
GPIO.setwarnings(False)

WAIT = 0.03
try:
    WAIT = float(argv[1])
except Exception:
    pass

def main(WAIT):
    '''
    '''
    counter = 0
    total = 0
    while True:
        input_value = GPIO.input(17)
        sleep(WAIT)
        if input_value == 0:
            counter += 1
            print("======================== PULSE " + str(total))
            total += 1
            pulse = open("/data/test.dat", "w")
            pulse.write(strftime("%H:%M:%S") + "," + str(1))
            pulse.close()
        else:
            counter = 0

if __name__ == '__main__':
    main(WAIT)
