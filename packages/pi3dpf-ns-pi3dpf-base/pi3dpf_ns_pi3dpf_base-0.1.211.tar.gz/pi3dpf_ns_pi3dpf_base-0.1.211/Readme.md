# Pre-requisites #
- Raspberry 3B+ or later
- [Raspberry Pi OS (32-bit)](https://www.raspberrypi.org/downloads/raspberry-pi-os/) with desktop and recommended software
- [OpenWeatherMap](https://openweathermap.org/) API key (free, registration required)

# Installation #
Download pi3d-pictureframe Debian package from here

Install pi3d-pictureframe and its dependencies:

    sudo apt-get update && sudo apt-get full-upgrade # update OS
    cd /var/tmp; wget download-url # download debian package to install picture-frame package
    sudo apt-get -f install /var/tmp/pi3d-pictureframe_2020.0719.171252-20b0bf4_armhf.deb # install

    sudo raspi-config # change raspberry graphic system configuration
    1: set gpu_mem=128        (Option 7 > A3 > Enter 128 or 256)
    2: enable FAKE KMS driver (Option 7 > A8 > G2)

# Basic Configuration #

**/home/pi/.pf/pf.config**

This is the main configuration file. You want to change the cities, language and units used to display  weather information provided by OpenWeatherMap.

Edit the file: `vi /home/pi/.pf/pf.config`, then add:

    [DEFAULT]
    #find your city ID: http://bulk.openweathermap.org/sample/city.list.json.gz
    OWM_CITY_IDS : 2657896:de ; Zurich, Switzerland. Show weather description in German
	OWM_UNITS : metric ; use 'metric' for °C or 'imperial' for °F
	
	CEC_CONTROL_TV                 : no ; if you do not wish the TV turns on when picture frame starts
	MQTT_SERVER_NAME               : egnor.nyx.net ; use your MQTT server name instead



**Notes:** 

- on above 'vi' command, use 'i' to insert text, ':wq' the save pf.config
- pf.config parameter values can be assigned using colon (:) or equal sign (=)
- comments can be made using hash (#) or semi-colon (;). For in-line comments, always use (;)
- You may change arbitrary default values by perusing [/opt/venvs/pi3d-pictureframe/lib/python3.7/site-packages/pi3dpf/cfg/pf.config](pi3dpf_ns/pi3dpf_base/cfg/pf.config), copy parameter names to `/home/pi/.pf/pf.config` and change their values.
- Beware using dns names (e.g. egnor.nyx.net) in MQTT_SERVER_NAME. If service does not start after reboot, use IP address instead.

**/home/pi/.pf/pf_secrets**

This file holds **your** API keys and passwords. `pf.config` parameters with their values prefixed with `!SECRET` will retrieve their effective values from `pf_secrets`. 

Example:

 `OWM_API_KEY                    : !SECRET owm_api_key ; origin: pf.config`

Edit the file: `vi /home/pi/.pf/pf_secrets`, then add:

    mqtt_password: mqtt-secret
    owm_api_key: register-and-get-your-own-key

**Notes:** 


- Above example demonstrates how the `pf.config` parameter `OWM_API_KEY` is configured to get the value `register-and-get-your-own-key`. All you need to do is adding your API key to `pf_secrets`.
- you need to supply your own `owm_api_key`. 
- changes to `/home/pi/.pf/pf.config` and `/home/pi/.pf/pf_secrets` take effect upon application restart.
- More on mqtt clients and mqtt_password in MQTT section.

# Starting Picture Frame from the Command Line #

Should you prefer starting the picture frame using MQTT, skip to the next section.
 
As user **pi**, on **RPi3B+**:

    pi@campero:~ $ source /opt/venvs/pi3d-pictureframe/bin/activate
    (pi3d-pictureframe) pi@campero:~/pi3d_demos $ PictureFrame2020.py --help # show available options
    (pi3d-pictureframe) pi@campero:~ $ pictureframe.sh -h # show available options from helper script
    (pi3d-pictureframe) pi@campero:~ $ pictureframe.sh -a pic-start -r -d /path/to/pictures

As user **pi**, on **RPi4**:

     pi@durin:~ $ sudo su - 
     root@durin:~# source /opt/venvs/pi3d-pictureframe/bin/activate
     (pi3d-pictureframe) root@durin:~# pictureframe.sh -a pic-start -d /path/to/pictures

**Notes:**

- you may place additional PictureFrame2020.py command line options into `/home/pi/.pf/PictureFrame2020.cli_opts`
- picture frame will be started in the background. Use `tail -f /home/pi/.pf/logs/PictureFrame2020.log` the check for errors. On rare occasions, check `tail -f /home/pi/.pf/logs/PictureFrame2020_mqtt.log`.
- see more convenient means to control picture frame in MQTT sections

# MQTT Broker #

For MQTT to work, you need to connect above MQTT clients to a MQTT message broker. Home Automation software such as Home Assistant, openHAB and others will work but mind the learning curve...

You may want to install the MQTT message broker `mosquitto` on your RPi using the command `sudo apt-get install mosquitto`

# MQTT Clients #

The package pi3d-pictureframe comes with two MQTT clients:

- The one built into `PictureFrame2020.py`, which is enabled by adding the options `--mqtt_server MQTT_SERVER`, `--mqtt_port MQTT_PORT`, `--mqtt_login MQTT_LOGIN` and `--mqtt_password MQTT_PASSWORD` to `/home/pi/.pf/PictureFrame2020.cli_opts`.
- The one provided with `mqtt-for-pi3dpf.py`. This service allows you to control PictureFrame2020.py and additional components, e.g. Hyperion.  

The `mqtt-for-pi3dpf.py` service can be enabled as follows:

    sudo systemctl unmask mqtt-for-pi3dpf.service
    sudo systemctl enable mqtt-for-pi3dpf.service
    sudo systemctl start  mqtt-for-pi3dpf.service
    sudo systemctl status mqtt-for-pi3dpf.service
    
**Note:**

- Above systemctl commands need to be executed after reinstalling or upgrading pi3d-pictureframe
- If you wish to always start mqtt-for-pi3dpf.service, execute `touch /home/pi/.pf/start.mqtt-for-pi3dpf.service`.

`mqtt-for-pi3dpf.py` subscribes to the following MQTT topics:

- start/stop the displaying of pictures 
- start/stop the normal desktop
- show list of 
- status and help

Checking log file:

    tail -f /home/pi/.pf/logs/mqtt-for-pi3dpf.log


# Further Topics #

**Software**

- Configuration Options on a per Picture Folder Basis and more (not done yet)
- Home Assistant Integration (not done yet)
- Image Scrapers (not done yet)

**Hardware**

- [Hyperion, Wake up light](doc/Hyperion.and.Wake-up-light.md)
- Presence detection, temperature and humidity measurement, room brightness sensor (not done yet)

# Credits #

- Wolfgang Männel for getting me started on pi3d pictureframe on his [web site](https://www.thedigitalpictureframe.com/how-to-add-crossfading-slide-transitions-to-your-digital-picture-frame-using-pi3d/)
- Thanks for Paddy Gaunt from the pi3d team for writing PictureFrame2020.py
 