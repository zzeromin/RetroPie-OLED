# RetroPie-OLED
Show Game Title on 128x64 OLED I2C Display for RetroPie v4.0.2+

<img src="https://github.com/zzeromin/RetroPie-OLED/blob/master/RetroPie-OLED01.jpg" width="70%" height="70%">

## About
This script written in Python for RetroPie project (https://retropie.org.uk/) 
running on Raspberry Pi 2,3, which displays all necessary info on a 128x64 OLED I2C display

## Features
* Current Date and Time, IP address of eth0, wlan0
* CPU Temperature and Speed
* Emulation and ROM information
* Double-byte character set support (Korean/Chinese/Japanese)

## Development Environment
* Raspberry Pi 2, 3
* RetroPie v4.0.2 and later
* 128x64 OLED I2C display

## Install

First, you should install Scraper( https://github.com/retropie/retropie-setup/wiki/scraper )

Second, Install below:
<pre><code>cd /home/pi
git clone https://github.com/zzeromin/RetroPie-OLED.git
cd /home/pi/RetroPie-OLED/
chmod 755 11.OLED.sh
sudo ./11.OLED.sh
</code></pre>

* Raspberry Pi I2C GPIO Pinout

![Alt text](https://i.imgur.com/WTPHzsf.png)
