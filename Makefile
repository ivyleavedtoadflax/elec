

build: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build -t elec:latest .

build_new: Dockerfile src/read_led.py src/requirements.txt
	sudo -E docker build --no-cache -t elec:latest .

run:
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
	-it elec:latest test.py

#-c '../tests/test.py'

clean:
	-sudo docker stop $$(sudo docker ps -aq) && \
	sudo docker rm $$(sudo docker ps -aq)

help:
	@cat Makefile

.PHONY: build build_new run test clean help
