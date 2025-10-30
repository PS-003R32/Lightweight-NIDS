# Lightweight-NIDS [Randomforest using scikit-learn]
This is the new phase of the development process of the NIDS. This uses `randomforest classifier` using `scikit-learn` to detect network anomalies. You can navigate to the root dir of this repository and choose an appropriate
one based on your requirements. For all the three phases of development of this nids I have used the same hardware for you to follow along easily.

---
## Hardware
- Raspberry Pi Zero 2W
- 1602 LCD module
- SSD1306 OLED module
- jumperwires and breadboard (if you need)

## Hardware setup
<p align="center">
  <img src="https://github.com/user-attachments/assets/e3c6f7a7-27d1-463e-ac2a-4967c7eea3d7" alt="GPIO-Pinout-Diagram" width="40%" />
  <img src="https://github.com/user-attachments/assets/05ccac08-1b31-4d38-a6ef-6b8f96fd70c5" alt="displays" width="40%" />
</p>

Open a terminal on the rpi and use the `sudo raspi-config` then navigate to Interfaces to enable I2C connection. 
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

*Once you wire the hardware, verify the connection `sudo i2cdetect -y` this should display a grid of memory address, LCD should have 0x27 and the oled should have 0x3C memory address.*
