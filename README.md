# Lightweight-NIDS
This project is a lightweight network intrution detection system which utilizes `hping3` as a subprocess and using a python script to simulate an IDS on a raspberry pi. I have used two displays, one for the nids console and another for displaying potential attacker's IP address. Please note this project is for simulation purpose and is under contineous improvement. 
You can find the snapshots of the NIDS in action in the `snapshots` dir.

## Hardware
- Raspberry Pi Zero 2W
- 1602 LCD module
- SSD1306 OLED module
- jumperwires and breadboard (if you need)

## Hardware setup
![GPIO-Pinout-Diagram](https://github.com/user-attachments/assets/e3c6f7a7-27d1-463e-ac2a-4967c7eea3d7) <br>

Using jumper wires on a bread board connect:<br>
[NOTE: the serial data and clock will be shared for both the displays.]
### SSD1306
- SDA to Pin 3 on rpi.
- SCL to Pin 5.
- GND to Pin 6.
- VCC to pin 1.
### 1602 LCD
- SDA to pin 3.
- SCL to pin 5.
- GND to pin 9.
- VCC to Pin 2.

## Script
You can find the python script in this repository itself. Copy the code and run `sudo python3 lwnids.py` and it will initialize the setup.

## Testing
After connecting the raspberry pi and your pc to the same network find the IP address of the rpi. Now send flood the rpi with ping requests from the windows pc : `ping 10.162.241.188 -t`.
You will see the rpi detects it and displays alerts on both the displays.
- The SSD1306 oled module will display potential attacker's IP address.
- 1602 LCD module will display the NIDS program console.
