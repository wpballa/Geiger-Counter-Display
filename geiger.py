#! /usr/bin/python3

# Written by Bill Ballard January 2018 for MightyOhm Geiger counter
# interface to Raspberry Pi with a Pimoroni scrollpHat or scrollpHatHD
# Designed to run in python3
# python3 geiger.py &
#
# Hardware setup
# connect scrollpHat to the GPIO, then connect
# Pi GPIO pin 6 to Geiger J7 pin 1
# Pi GPIO pin 8 to Geiger J7 pin 4
# Pi GPIO pin 10 to Geiger J7 pin 5
#
# Software setup, after update/upgrade
# sudo apt-get install python3-pip (if using Stretch lite)
# sudo pip3 install pySerial
#
# for older 5x11 Pimoroni Scroll pHat version
# sudo apt-get install python3-scrollphat
#
# or for newer HD version
# sudo apt-get install python3-scrollphathd
#
# set this line according to your version of the scroll pHat

HD = True          # set to true for HD version, false for old version

#
# sudo nano /boot/cmdline.txt
# and remove the console=serial0,115200 save and reboot
# 
# License: GPL 2.0

# load all the modules we will need

import serial
import time

if (HD):
    import scrollphathd
    from scrollphathd.fonts import font5x7
else:
    import scrollphat

# file name for logging data, customize as you wish but use full path
# in case you background the job at boot

fname = "/home/pi/geiger.csv"

# open the mightyohm geiger counter terminal

ser = serial.Serial('/dev/ttyAMA0', baudrate=9600)

# initialize scrollphathd or scrollphat

if (HD):
    scrollphathd.set_brightness(0.2)
    scrollphathd.rotate(180)
    scrollphathd.clear()
else:
    scrollphat.set_brightness(32)
    scrollphat.set_rotate(True)
    scrollphat.clear()

# read each line of input, reformat byte to string and write to file
# note that the decode trick is hard to find in Python documentation!

while True:
    try:
        lin=ser.readline()
        line=lin.decode('utf-8').split(',')
        outs = line[5] + line[4]
        print(outs)
        if (HD) :
            scrollphathd.clear()
            scrollphathd.write_string(outs, x=1, y=0, font=font5x7)
            (buf1, buf2) = scrollphathd.get_buffer_shape()
            for i in range(buf1):
                scrollphathd.show()
                scrollphathd.scroll()
                time.sleep(0.1)
        else:
            scrollphat.clear()
            scrollphat.write_string(outs, 11)
            len = scrollphat.buffer_len()
            for i in range (len):
                scrollphat.scroll()
                time.sleep(0.1)

# now write to file, close each time in case you stop the program

        geig = open(fname, 'a')
        geig.write(lin.decode('utf-8'))
        geig.close()

    except (KeyboardInterrupt, SystemError, SystemExit): #reasons to stop
        if (HD):
            scrollphathd.clear()
        else:
            scrollphat.clear()
        geig.close()
        ser.close()
