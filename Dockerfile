FROM resin/rpi-raspbian:latest

# Note that this container can only be built on ARM architecture!

MAINTAINER Matthew Upson
LABEL date="2018-02-03"
LABEL version="2.0.0"
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

# Set arguments that must be passed in the build command e.g.:
# sudo docker build --build-arg MQTT_HOST=${MQTT_HOST}

ARG MQTT_HOST
ARG MQTT_PORT
ARG MQTT_USERNAME
ARG MQTT_PASSWORD
ARG MQTT_TOPIC
ARG MQTT_QOS
ARG ELEC_INTERVAL
ARG ELEC_LOG
ARG ECONOMY7
ARG DAY_START
ARG NIGHT_START
ARG DAY_RATE
ARG NIGHT_RATE
ARG PULSE_UNIT

# Set environment variables: these will be passed into the container

ENV MQTT_HOST $MQTT_HOST
ENV MQTT_PORT $MQTT_PORT
ENV MQTT_USERNAME $MQTT_USERNAME
ENV MQTT_PASSWORD $MQTT_PASSWORD
ENV MQTT_TOPIC $MQTT_TOPIC
ENV MQTT_QOS $MQTT_QOS
ENV ELEC_INTERVAL $ELEC_INTERVAL
ENV ELEC_LOG $ELEC_LOG
ENV ECONOMY7 $ECONOMY7
ENV DAY_START $DAY_START
ENV NIGHT_START $NIGHT_START
ENV DAY_RATE $DAY_RATE
ENV NIGHT_RATE $NIGHT_RATE
ENV PULSE_UNIT $PULSE_UNIT

# Run read_led.py at launch

ENTRYPOINT ["python3"]

CMD ["read_led.py"]
