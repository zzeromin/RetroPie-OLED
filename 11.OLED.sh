## 11.OLED.sh
# Title        : RetroPie-OLED
# Author       : zzeromin, member of Raspberrypi Village
# Creation Date: Nov 13, 2016
# Blog         : http://rasplay.org, http://forums.rasplay.org/, https://zzeromin.tumblr.com/
# Thanks to    : smyani, zerocool, superstar
# Free and open for all to use. But put credit where credit is due.
#
# Install      :
# cd /home/pi
# git clone https://github.com/zzeromin/RetroPie-OLED.git
# cd /home/pi/RetroPie-OLED/
# chmod 755 11.OLED.sh
# sudo ./11.OLED.sh
#
# Reference    :
# https://github.com/ipromiseyou/RetroPie-AutoSet.git

cd /home/pi/RetroPie-OLED/
cp runcommand-onstart.sh /opt/retropie/configs/all/
cp runcommand-onend.sh /opt/retropie/configs/all/
sed -i '1i\\/usr/bin/python /home/pi/RetroPie-OLED/RetroPie-OLED.py &' /opt/retropie/configs/all/autostart.sh
echo "OLED Setup Complete."
echo "I2C, Python Tools Setup are starting now"
sleep 1
apt-get install -y python-pip python-imaging python-dev python-smbus i2c-tools
echo "i2c-bcm2708" >> /etc/modules
echo "i2c-dev" >> /etc/modules
sed -i 's/#dtparam=i2c_arm/dtparam=i2c_arm/' /boot/config.txt
echo "I2C, Python Tools Setup Complete."
echo "Adafruit_Python_SSD1306 Setup is starting now"
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
python setup.py install
chgrp -R -v pi /home/pi/RetroPie-OLED
chown -R -v pi /home/pi/RetroPie-OLED
chgrp -R -v pi /opt/retropie/configs/all
chown -R -v pi /opt/retropie/configs/all
echo "All Setup Complete. Reboot after 3 Seconds."
sleep 3
reboot
