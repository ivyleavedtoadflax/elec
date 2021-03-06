FROM resin/rpi-raspbian:latest

# Note that this container can only be built on ARM architecture!

LABEL maintainer="Matthew Upson"
LABEL date="2018-04-23"
LABEL version="2.5.0"
LABEL description="Measure electricity usage with a raspberry pi"

# Prepare for using gpio

RUN apt-get -qy update \
    && apt-get -qy install \
    python3 python3-pip \
    python3-dev gcc make

COPY ./src src

# Set working directory

WORKDIR /src

# Install python requirements

RUN pip3 install -r requirements.txt

# Set environment variables: these will be passed into the container
# and must be populated at runtime with --env-file or -e

ENV MQTT 0
ENV MQTT_HOST 192.168.1.14
ENV MQTT_PORT 1883
ENV MQTT_USERNAME mosquitto
ENV MQTT_PASSWORD ''
ENV MQTT_TOPIC tele/electricity/
ENV MQTT_QOS 1
ENV ELEC_INTERVAL 30
ENV ELEC_LOG /data/elec.log
ENV ECONOMY7 0
ENV DAY_START 07:30
ENV NIGHT_START 22:30
ENV DAY_RATE 0.15158
ENV NIGHT_RATE 0.15158
ENV PULSE_UNIT 0.00025
ENV DURATION 0.005

# Run read_led.py at launch

ENTRYPOINT ["python3"]

CMD ["read_led.py"]
