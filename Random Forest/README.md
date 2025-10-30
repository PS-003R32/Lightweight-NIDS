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
  <img src="https://github.com/user-attachments/assets/e3c6f7a7-27d1-463e-ac2a-4967c7eea3d7" alt="GPIO-Pinout-Diagram" width="30%" />
  <img src="https://github.com/user-attachments/assets/05ccac08-1b31-4d38-a6ef-6b8f96fd70c5" alt="displays" width="27%" />
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

---
# Training
You can use the pickle files in this repository directly or train with wour own dataset using the python script in this repository.
### Using pretrained
Create a new directory in the zero 2w and place the two pickle files, `encoders.pkl` and `nids_model.pkl`, along with the `rpiscript.py` in the same directory and run the script, `sudo python3 rpiscript.py`.<br>
Let the rpi load the model, you will see it in the cli aswell as the lcd display. After it loads completely open a terminal on your windows pc and flood the rpi with large sized icmp ping req packets, `ping <I.P. of rpi> -t -l 65535`. This will trigger the model running on the pi to detect the attack and display it on the two displays connected to the rpi aswell as the terminal window on the rpi.<br>

### Train with your own data
To train the model using your own data you can use the python script in the `Model Trainer/trainer.py` to train with your own dataset. To do this rename the `csv` data set path in the `trainer.py` script to generate `pkl` files. then the process is same as mentioned in the above section.

---
You can check out the working snaps of the model in action in the snaps dir.
