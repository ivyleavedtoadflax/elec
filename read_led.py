'''
Read a blinking LED and log
'''

#!/usr/bin/env python

import os
import json
from time import strftime, sleep, time
import RPi.GPIO as GPIO
from paho.mqtt.publish import single

######################### Setup GPIO PINS #########################

# Use Broadcom chip reference for GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Name pins

LDR_PIN = 17    # LDR (light dependent resistor)
LED_PIN = 0     # LED (light emitting diode)

GPIO.setup(LDR_PIN, GPIO.IN)

# Get MQTT server credentials from environment vars

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
ELEC_INTERVAL = int(os.environ.get('ELEC_INTERVAL'))
ELEC_LOG = os.environ.get('ELEC_LOG')

#Define functions

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

def write_log_csv(timestamp, value, log_file=ELEC_LOG):
    '''
    Write log data to csv

    :param timestamp: <str> Timestamp
    :param value: <int> Value (count of flashes)
    :param log_file: <str> Location of log file
    '''

    log = open(log_file, "a")
    log.write("\n" + str(timestamp) + "," + str(value))
    log.close()

def main(interval=ELEC_INTERVAL):


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

        sensor_data = {
            "Time" : timestamp,
            "Pulses" : counter
        }

        sensor_data = json.dumps(sensor_data)
    # Try to log to csv

        try:
            write_log_csv(timestamp, counter)
        except Exception:
            pass

        try:
            single(
                topic=MQTT_TOPIC, payload=sensor_data, qos=1,
                hostname=MQTT_HOST, port=MQTT_PORT,
                auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
                )

        except Exception:
            print('Failed to send message to MQTT broker')

if __name__ == '__main__':
    main()

GPIO.cleanup()

