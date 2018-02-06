
build:
	sudo -E docker build \
	--build-arg MQTT_PORT=${MQTT_PORT} \
	--build-arg MQTT_HOST=${MQTT_HOST} \
	--build-arg MQTT_TOPIC=${MQTT_TOPIC} \
	--build-arg MQTT_USERNAME=${MQTT_USERNAME} \
	--build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
	--build-arg ELEC_INTERVAL=${ELEC_INTERVAL} \
	--build-arg ELEC_LOG=${ELEC_LOG} \
	--build-arg ECONOMY7=${ECONOMY7} \
	--build-arg DAY_START=${DAY_START} \
	--build-arg NIGHT_START=${NIGHT_START} \
	-t elec:latest .

build_new:
	sudo -E docker build \
	--build-arg MQTT_PORT=${MQTT_PORT} \
	--build-arg MQTT_HOST=${MQTT_HOST} \
	--build-arg MQTT_TOPIC=${MQTT_TOPIC} \
	--build-arg MQTT_USERNAME=${MQTT_USERNAME} \
	--build-arg MQTT_PASSWORD=${MQTT_PASSWORD} \
	--build-arg ELEC_INTERVAL=${ELEC_INTERVAL} \
	--build-arg ELEC_LOG=${ELEC_LOG} \
	--build-arg ECONOMY7=${ECONOMY7} \
	--build-arg DAY_START=${DAY_START} \
	--build-arg NIGHT_START=${NIGHT_START} \
	--no-cache -t elec:latest .

run:
	sudo docker run -v /data:/data \
        --privileged --name elec \
        --restart unless-stopped \
        -td elec:latest

test:
	sudo docker run -v /data:/data \
        --name test -t elec:latest \
        -c 'print("****** Hello World! ******")' && \
    sudo docker rm test

clean:
	-sudo docker stop $$(sudo docker ps -aq) && \
	sudo docker rm $$(sudo docker ps -aq)

help:
	@cat Makefile

.PHONY: build build_new run test clean help
