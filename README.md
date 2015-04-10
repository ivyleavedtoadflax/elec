# elec

## Instructions for set up

* Establish headless wifi connection with pi
* sudo apt-get update -y
* sudo apt-get upgrade -y
* sudo apt-get install postgresql-9.1 libpq-dev python-dev python-pip
* sudo pip install psycopg2
* sudo pip install dropbox
* add a server_cred.py file with the following lines:
    * db_name = ''
    * host_ip = ''
    * username = ''
    * password = ''
* add dropbox access token in access_token.py as token=''
* add the following lines to crontab with crontab -e
    * @reboot sudo python ~/elec/read_led.py
    * @reboot sudo python ~/elec/db.py
    * * 2 * * * sudo python ~/elec/db.py
