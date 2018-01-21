# raspi-elec

This repository contains code for setting up a raspberry pi pulse counter for reading led pulses from an electricity meter.

## Instructions for set up

Currently this has only been tested on ~~[Raspbian Wheezy 2015-05-05](https://www.raspberrypi.org/downloads/raspbian/)~~ [Raspbian Jessie 2015-09-24](https://www.raspberrypi.org/downloads/raspbian/) installed from the img, not using NOOBS.


## Instructions for setup

### Connecting to WiFi

* Install raspbian-wheezy 2015-05-05
   * Follow the instructions [here]([Rasbian Wheezy 2015-05-05](https://www.raspberrypi.org/downloads/raspbian/))
* Establish headless wifi connection with pi
   * make sure SSH is enabled
   * because I don't like to connect my pis to monitors (it's a bit of a pain), I pre-install the /etc/wpa_supplicant/wpa_supplicant.cong file on the SD card with the settings from my wifi router. Then i can get online headlessly without trouble. The settings for my wifi network are as follows, yous may be similar:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev

network={
   ssid="my-base-station-ssid"
   psk="my-password"
   proto=RSN
   key_mgmt=WPA-PSK
   pairwise=CCMP
   auth_alg=OPEN
}

```
### Environment Variables

Setting environmental variables. The following env vars need to be set on the raspberry pi.
*Note that in v1.1.0 these is not implemented, and indtead these values are hardcoded. This is because the pi was failing to find the environment vars at logon, despite being placed in the `/etc/profile` file.*


|Variable|Definition|
|---|---|
|ELEC_LOG|File path for pulse data log file|
|ELEC_INTERVAL|Interval over which electricity measurements are taken|
|MQTT_HOST|MQTT broker hostname|
|MQTT_PORT|MQTT broker port|
|MQTT_USERNAME|MQTT account username|
|MQTT_PASSWORD|MQTT account password|
|MQTT_TOPIC|MQTT topic on which to publish|

### Running the script automatically

* Add the following lines to crontab with crontab -e.
* Starts python pulse logging script on reboot.

```
@reboot sudo python ~/elec/read_led.py
```

## Circuit for pulse counting

The pulse counting circuit is built using a light dependent resistor.
When there is a pulse, the resistance in the circuit decreases, and this is recorded.
Initially I was recording this is a very simple circuit using just a capacitor connected to one of the GPIO pins ([see an excellent overview on how to do this here](https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/overview)), but eventually I transitioned to using a more complicated circuit which outputs a single pulse with each flash of the LED, and not a count of time taken to fill a capacitor (as in the simpler circuit).

Here I have drawn heavily on [this rep](https://github.com/kieranc/power), and in turn [this blog](http://blog.christianperone.com/2012/08/raspberry-pi-arduino-a-laser-pointer-communication-and-a-ldr-voltage-sigmoid/).

Breadboard setup:

![breadboard.jpg](breadboard.jpg)

Rasbpi setup

![raspiaplus.jpg](raspiaplus.jpg)

## Some testing

I was skeptical that using an LDR (which can be quite slow) would be quick enough to detect flashes over a fraction of a second, so I tested this using the file [test_led.py](test_led.py).
By setting the pi to execute a number of blinks, with random intervals, and counting them back using the pulse counter, I found the LDR to have perfect accuracy over a range of conditions (which sadly I did not record at the time!).

Two test scripts are included, both of which are launched from the command line.

The first [test.py](test.py) can be launched with `sudo python test.py` with an optional argument of the sleep time between measurements (if not specified, this defaults to 0.03 seconds).
The second file [test_led.py](test_led.py) can be used in conjunction with test.py, by directing the LDR at the indicator LED on the breadboard.
test_led.py takes three arguments e.g.: `sudo python test_led.py 10 0.1 10`. These are:

* Number of flashes
* Duration of flash in seconds
* Maximum interval from which a random number will be selected

By adjusting these arguments, you can simulate the kind of flashes that you would receive from your meter, and test whether you are receiving them properly using the [test.py](test.py) script.

