# Lightweight-NIDS
This project is a lightweight network intrution detection system which utilizes `hping3` as a subprocess and using a python script to simulate an IDS on a raspberry pi. Please note this project is for simulation purpose
and is under contineous improvement. 

## Hardware
- Raspberry Pi Zero 2W
- 1602 LCD module
- SSD1306 OLED module
- jumperwires and breadboard (if you need)

## Hardware setup

## Script
You can find the python script in this repository itself. Copy the code and run `sudo python3 lwnids.py` and it will initialize the setup.

## Testing
After connecting the raspberry pi and your pc to the same network find the IP address of the rpi. Now send flood the rpi with ping requests from the windows pc : `ping 10.162.241.188 -t`.
You will see the rpi detects it and displays alerts on both the displays.
