#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Title        : RetroPie_OLED.py
Author   : zzeromin, member of Raspberrypi Village
Creation Date: Nov 13, 2016
Blog        : http://rasplay.org, http://forums.rasplay.org/, https://zzeromin.tumblr.com/
Thanks to    : smyani, zerocool, GreatKStar
Free and open for all to use. But put credit where credit is due.

Reference    :
https://github.com/adafruit/Adafruit_Python_SSD1306.git
https://github.com/haven-jeon/piAu_volumio

Notice       :
installed python package: python-pip python-imaging python-dev python-smbus i2c-tools
This code edited for rpi3 Retropie v4.0.2 and later by zzeromin
"""

import time
import os
from sys import exit
from subprocess import *
from time import *
from datetime import datetime

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

def run_cmd(cmd):
# runs whatever is in the cmd variable in the terminal
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_ip_address(cmdeth):
    # ip & date information
    ipaddr = run_cmd(cmdeth)
    return ipaddr

def get_cpu_temp():
    tempFile = open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_mem_cap():
    mem_avail = run_cmd("df / -h | grep '/' | awk '{print $4}'")
    mem_used = run_cmd("df / -h | grep '/' | awk '{print $3}'")
    sdmem = mem_used.replace("\n","") + "/" +  mem_avail.replace("\n","")
    return sdmem

import signal
def exit_msg(signal, frame):
    disp.begin()
    # Clear display.
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    font_system = ImageFont.truetype('/root/RetroPie-OLED/neodgm.ttf', 16)
    msg = "그만 끄고 자시오"
    msg = unicode(msg)
    msg_length = len(msg)
    msg_size = draw.textsize(msg, font=font_system)
    msgwrap = textwrap.wrap(msg, width=8)
    current_h, text_padding = 22, 2
    draw.rectangle((0,0,width,height), outline=0, fill=0 )
    for line in msgwrap:
        msgwrap_size = draw.textsize(line, font=font_system)
        draw.text(((width - msgwrap_size[0])/2, current_h), line, font=font_system, fill=255)
                
        current_h += msgwrap_size[1] + text_padding
    disp.image(image)
    disp.display()
    sys.exit()

signal.signal(signal.SIGTERM, exit_msg)
signal.signal(signal.SIGINT, exit_msg)

def main():

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.

    padding = 0
    top = padding
    bottom = height-padding

    # Load default font.
    font_system = ImageFont.truetype('/root/RetroPie-OLED/neodgm.ttf', 16)
    font_rom = ImageFont.truetype('/root/RetroPie-OLED/BM-HANNA.ttf', 16)
    fonte_rom = ImageFont.truetype('/root/RetroPie-OLED/lemon.ttf', 10)

    #get ip address of eth0 connection
    cmdeth = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    #get ip address of wlan0 connection
    #cmd = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"

    #get ip address of eth0 connection    
    ipaddr = get_ip_address(cmdeth)
    ipaddr = ipaddr.replace("\n","")

    old_Temp = new_Temp = round(get_cpu_temp(),1)
    
    mem_cap = get_mem_cap()    
    title = "title"

    while True:
        try:
            titleimg = Image.open("/root/RetroPie-OLED/" + title + ".png").convert('1')
            # except FileNotFoundError:
        except IOError:
            new_Temp = round(get_cpu_temp(),1)
            ipaddr = get_ip_address(cmdeth)
            ipaddr = ipaddr.replace("\n","")
            if len(ipaddr) > 0 :
                ipaddr = "IP " + ipaddr
            ipaddr_size = draw.textsize(ipaddr, font=fonte_rom)
            
            if old_Temp != new_Temp :
                old_Temp = new_Temp

            info = mem_cap + "  " + str( new_Temp ) + chr(0xB0) +"C"
            info_size = draw.textsize(info, font=fonte_rom)

            msg = "팬더스테이션3+"
            msg = unicode(msg)
            msg_length = len(msg)
            msg_size = draw.textsize(msg, font=font_system)
            msgwrap = textwrap.wrap(msg, width=10)
            
            current_h, text_padding = 22, 2
            
            draw.rectangle((0,0,width,height), outline=0, fill=0 )
            #icon = "icon"
            #icon = Image.open("/root/RetroPie-OLED/" + icon + ".png") 
            #image.paste(icon,(0,0))

            for line in msgwrap:
                msgwrap_size = draw.textsize(line, font=font_system)
                draw.text(((width - msgwrap_size[0])/2, current_h), line, font=font_system, fill=255)
                
                current_h += msgwrap_size[1] + text_padding
            draw.text(((width - info_size[0])/2  , top+46), info , font=fonte_rom, fill=255)
            #draw.text((96, top+54), info , font=fonte_rom, fill=255)
            draw.text(((width - ipaddr_size[0])/2, top+54), ipaddr, font=fonte_rom, fill=255)
            disp.image(image)
            disp.display()
            sleep(3)
            pass
        else:
            image.paste(titleimg,(0,0))
            disp.image(image)
            disp.display()
            sleep(3)


if __name__ == "__main__":
    import sys

    try:
        main()

    # Catch all other non-exit errors
    except Exception as e:
        sys.stderr.write("Unexpected exception: %s" % e)
        sys.exit(1)

    # Catch the remaining exit errors
    except:
        sys.exit(0)
