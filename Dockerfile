FROM resin/rpi-raspbian:latest

# Note that this container can only be built on ARM architecture!

MAINTAINER Matthew Upson
LABEL date="2018-02-03"
LABEL version="0.1.0"
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
ARG ELEC_INTERVAL
ARG ELEC_LOG

# Set environment variables: these will be passed into the container

ENV MQTT_HOST $MQTT_HOST
ENV MQTT_PORT $MQTT_PORT
ENV MQTT_USERNAME $MQTT_USERNAME
ENV MQTT_PASSWORD $MQTT_PASSWORD
ENV MQTT_TOPIC $MQTT_TOPIC
ENV ELEC_INTERVAL $ELEC_INTERVAL
ENV ELEC_LOG $ELEC_LOG

# Run read_led.py at launch

ENTRYPOINT ["python3"]

CMD ["read_led.py"]
