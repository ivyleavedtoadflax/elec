PWD = $(shell pwd)

all: clean telegraf.conf elec run telegraf

telegraf.conf: telegraf.template.conf .envrc Makefile
	echo "Creating telegraf.conf file"; \
	sed -e "s/\$${DATABASE}/$(DATABASE)/" \
	-e "s%\$${INFLUXDB_HOST}%$(INFLUXDB_HOST)%" \
	-e "s/\$${INFLUXDB_PORT}/$(INFLUXDB_PORT)/" \
	-e "s/\$${INTERVAL}/$(INTERVAL)/" \
	-e "s/\$${HOSTNAME}/$(HOSTNAME)/" \
	-e "s%\$${ELEC_LOG}%$(ELEC_LOG)%" \
	telegraf.template.conf > telegraf.conf

telegraf:
	sudo docker run \
	-d --restart unless-stopped \
	-v $(PWD)/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
	--name telegraf \
	-it telegraf:latest

elec: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build -t elec:latest .

elec_new: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build --no-cache -t elec:latest .

run:
	sudo docker run -v /data:/data \
        --privileged --name elec \
        --restart unless-stopped \
	--env-file .env \
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
