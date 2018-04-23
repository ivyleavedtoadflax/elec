PWD = $(shell pwd)

all: build telegraf.conf clean telegraf elec

telegraf.conf: telegraf.template.conf .envrc Makefile
	echo "Creating telegraf.conf file"; \
	sed -e "s/\$${DATABASE}/$(DATABASE)/" \
	-e "s%\$${INFLUXDB_HOST}%$(INFLUXDB_HOST)%" \
	-e "s/\$${INFLUXDB_PORT}/$(INFLUXDB_PORT)/" \
	-e "s/\$${INTERVAL}/$(INTERVAL)/" \
	-e "s/\$${HOSTNAME}/$(HOSTNAME)/" \
	-e "s%\$${ELEC_LOG}%$(ELEC_LOG)%" \
	telegraf.template.conf > telegraf.conf

telegraf: telegraf.conf
	sudo docker run \
	-d --restart unless-stopped \
	-v $(PWD)/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
	-v /data:/data:ro \
	--name telegraf \
	-it bradsjm/rpi-telegraf:latest

build: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build -t elec:latest .

build_new: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build --no-cache -t elec:latest .

elec:
	sudo docker run -v /data:/data \
        --privileged --name elec \
        --restart unless-stopped \
	--env-file .env \
        -td elec:latest

clean_test:
	-sudo docker stop test
	-sudo docker rm test

test:
	sudo docker run -v /data:/data \
        --privileged --name test \
	-it elec:latest test.py 0.01

clean:
	-sudo docker stop elec
	-sudo docker rm elec
	-sudo docker stop telegraf
	-sudo docker rm telegraf

help:
	@cat Makefile

.PHONY: telegraf build build_new run elec elec_test clean help
