'''
Read a blinking LED and log
'''

#!/usr/bin/env python

import os
from time import strftime, sleep, time
import RPi.GPIO as GPIO

######################### Setup GPIO PINS #########################

# Use Broadcom chip reference for GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Name pins

LDR_PIN = 17    # LDR (light dependent resistor)
LED_PIN = 0     # LED (light emitting diode)
LOG_FILE = os.environ.get('LOG_FILE')

GPIO.setup(LDR_PIN, GPIO.IN)

# Define functions

def get_light(ldr_pin, duration=0.03):
    '''
    Read from the GPIO pin then sleep

    :param ldr_pin: <int> Address of GPIO pin connected to light dependent resistor
    :param duration: <float> Duration in seconds that the rpi will sleep beyween measurements
    :return: <boolean>
    '''

    input_value = GPIO.input(ldr_pin)

    # Duration value can be experimented with
    # but 0.03 seems to be reasonable

    sleep(duration)
    if input_value == 0:
        output = 1
    else:
        output = 0
    return output

# Run data recording LED init sequence
# This is not currently used in this version

def led_flash(led_pin, n_flashes=2, interval=0.3):
    '''
    Flash an indicator LED

    :param LED_PIN: <int> Address of pin connected to LED
    :param n_flashes: <int> number of times to flash LED
    :param interval: <int> Interval between flashes (in seconds)
    '''

    count = 0
    while count < n_flashes:
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(interval)
        GPIO.output(led_pin, GPIO.LOW)
        sleep(interval)
        count += 1

def write_log_csv(timestamp, value, log_file=LOG_FILE):
    '''
    Write log data to csv

    :param timestamp: <str> Timestamp
    :param value: <int> Value (count of flashes)
    :param log_file: <str> Location of log file
    '''

    log = open(log_file, "a")
    log.write("\n" + str(timestamp) + "," + str(value))
    log.close()

def main(interval=60):
    '''
    Run the counter

    :param interval: <int> Recording interval (defaults to 60: one reading every minute)
    '''

    # Set the timeout to be the current time plus 60 seconds

    while True:
        timeout = time() + interval

    # Initiliase accumulator at zero
    # Then run get_light and add to accumulator
        counter = 0
        while timeout > time():
            counter += get_light(LDR_PIN)

        timestamp = strftime("%Y-%m-%d %H:%M:%S")

    # Try to log to csv

        try:
            write_log_csv(timestamp, counter)
        except Exception:
            pass

if __name__ == '__main__':
    main()

GPIO.cleanup()
