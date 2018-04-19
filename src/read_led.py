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

MQTT = int(os.environ.get('MQTT'))
MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
MQTT_QOS = int(os.environ.get('MQTT_QOS'))
ELEC_INTERVAL = int(os.environ.get('ELEC_INTERVAL'))
ELEC_LOG = os.environ.get('ELEC_LOG')
ECONOMY7 = int(os.environ.get('ECONOMY7'))
DAY_START = strftime(os.environ.get('DAY_START'))
NIGHT_START = strftime(os.environ.get('NIGHT_START'))
PULSE_UNIT = float(os.environ.get('PULSE_UNIT'))
DAY_RATE = float(os.environ.get('DAY_RATE'))
NIGHT_RATE = float(os.environ.get('NIGHT_RATE'))

# Print environment vars

print("*********** ENV VARS ***********")
print("MQTT:", MQTT)
print("MQTT_HOST:", MQTT_HOST)
print("MQTT_PORT:", MQTT_PORT)
print("MQTT_USERNAME:", MQTT_USERNAME)
print("MQTT_PASSWORD:", " *****", MQTT_PASSWORD[5:], sep="")
print("MQTT_TOPIC:", MQTT_TOPIC)
print("MQTT_QOS:", MQTT_QOS)
print("ELEC_INTERVAL:", ELEC_INTERVAL)
print("ELEC_LOG:", ELEC_LOG)
print("ECONOMY7:", ECONOMY7)
print("DAY_START:", DAY_START)
print("NIGHT_START:", NIGHT_START)
print("PULSE_UNIT:", PULSE_UNIT)
print("DAY_RATE:", DAY_RATE)
print("NIGHT_RATE:", NIGHT_RATE)

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

def write_json_log(timestamp, data, log_file=ELEC_LOG):
    '''
    Write log data to csv

    :param timestamp: <str> Timestamp
    :param value: <int> Value (count of flashes)
    :param log_file: <str> Location of log file
    '''

    try:
        with open(log_file, "a") as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print("Failed to log data to ", + "log_file")
        print(e)
        pass

def send_mqtt(data, mqtt_topic=MQTT_TOPIC, mqtt_qos=MQTT_QOS, 
              mqtt_host=MQTT_HOST, mqtt_port=MQTT_PORT, mqtt_username=MQTT_USERNAME, 
              mqtt_password=MQTT_PASSWORD):
    '''
    Send a single mqtt message
    '''

    try:
        single(
            topic=mqtt_topic, payload=data, qos=mqtt_qos,
            hostname=mqtt_host, port=mqtt_port,
            auth={'username': mqtt_username, 'password': mqtt_password}
            )

    except Exception as e:
        print('Failed to send message to MQTT broker')
        print(e)
        pass

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
        hour = strftime("%H:%M")
        night = 0

        if ECONOMY7:
            if hour > NIGHT_START or hour < DAY_START:
                night = 1

        rate = ((night * NIGHT_RATE) + ((1 - night) * DAY_RATE))
        cost = counter * PULSE_UNIT * rate
        cost = round(cost, 5)

        sensor_data = {
            "Time" : timestamp,
            "Pulses" : counter,
            "Night" : night,
            "Cost" : cost
        }

        # Try to log to json

        write_json_log(timestamp, sensor_data)

        # Try to log to MQTT

        if MQTT:

            mqtt_data = json.dumps(sensor_data)

            send_mqtt(mqtt_data, mqtt_topic=MQTT_TOPIC, mqtt_qos=MQTT_QOS, 
                      mqtt_host=MQTT_HOST, mqtt_port=MQTT_PORT, 
                      mqtt_username=MQTT_USERNAME, mqtt_password=MQTT_PASSWORD)

if __name__ == '__main__':
    main()

GPIO.cleanup()

