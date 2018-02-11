

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
