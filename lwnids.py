#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime
from collections import defaultdict
from RPLCD.i2c import CharLCD
import board
import busio
from digitalio import DigitalInOut
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import re

class LWNIDS:
    def __init__(self):
        # LCD setup
        self.lcd = CharLCD('PCF8574', 0x27)
        self.packet_types = {'ICMP': 0, 'ARP': 0, 'TCP': 0, 'UDP': 0}
        self.thresholds = {'ICMP': 15, 'TCP': 50, 'UDP': 40, 'ARP': 8}

        # OLED setup
        i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)
        self.oled.show()
        self.font = ImageFont.load_default()

        self.init_display()

    def init_display(self):
        self.lcd.clear()
        self.lcd.write_string("Ligthweight-NIDS")
        time.sleep(1)
        self.lcd.clear()
        self.lcd.write_string("Initializing...")
        time.sleep(1)
        self.log("Lw-NIDS READY")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def show_status(self, top_type, top_count):
        total = sum(self.packet_types.values())
        self.lcd.clear()
        self.lcd.write_string(f"{top_type:<4} COUNT:{top_count:3d}")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"TOTAL:{total:5d}")
        self.log(f"STATUS: {top_type}: {top_count} | TOTAL: {total}")

    def show_alert(self, alert_type, count, snapshot, attackers):
        # LCD alert
        self.lcd.clear()
        self.lcd.write_string("!!ALERT ACTIVE!!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"{alert_type} x{count:4d}")
        time.sleep(2)

        # LCD packet breakdown
        self.lcd.clear()
        keys = list(snapshot.keys())
        line1 = f"{keys[0]}:{snapshot[keys[0]]} {keys[1]}:{snapshot[keys[1]]}"
        line2 = f"{keys[2]}:{snapshot[keys[2]]} {keys[3]}:{snapshot[keys[3]]}"
        self.lcd.write_string(line1[:16])
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(line2[:16])
        time.sleep(2)

        # LCD final alert
        self.lcd.clear()
        self.lcd.write_string("SECURITY ALERT!!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"{alert_type} FLOOD")
        time.sleep(2)

        # OLED attacker IPs
        self.display_oled_alert(alert_type, attackers)

        # Console log
        self.log(f"SECURITY ALERT: {alert_type} FLOOD - {count} packets")
        self.log("Packet Breakdown:")
        for ptype, val in snapshot.items():
            self.log(f"  {ptype}: {val}")
        self.log("Attackers:")
        for ip, hits in attackers.items():
            self.log(f"  {ip}: {hits} packets")

    def display_oled_alert(self, alert_type, attackers):
        self.oled.fill(0)
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), f"ALERT:  {alert_type} flood", font=self.font, fill=255)
        draw.text((0,14), "Possible attacker IP", font=self.font, fill=255)

        draw.text((0,20), "", font=self.font, fill=255)
        y=30
        for ip, count in list(attackers.items())[:3]:  # Show top 3 IPs
            draw.text((0, y), f"{ip} : {count}", font=self.font, fill=255)
            y += 10
        self.oled.image(image)
        self.oled.show()

    def analyze_packets(self):
        result = subprocess.run(
            ['timeout', '4', 'tcpdump', '-i', 'any', '-n', '-c', '500'],
            capture_output=True, text=True
        )
        new_counts = {ptype: 0 for ptype in self.packet_types}
        attackers = defaultdict(int)

        for line in result.stdout.split('\n'):
            line_upper = line.upper()
            for ptype in new_counts:
                if ptype in line_upper:
                    new_counts[ptype] += 1
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+>\s+(\d+\.\d+\.\d+\.\d+)', line)
            if match:
                src_ip = match.group(1)
                attackers[src_ip] += 1

        for ptype in new_counts:
            self.packet_types[ptype] += new_counts[ptype]
        return new_counts, attackers

    def check_alerts(self, snapshot, attackers):
        for ptype, threshold in self.thresholds.items():
            if self.packet_types[ptype] > threshold:
                self.show_alert(ptype, self.packet_types[ptype], snapshot, attackers)
                return True
        return False

    def get_top_type(self):
        top_type = max(self.packet_types, key=self.packet_types.get)
        return top_type, self.packet_types[top_type]

    def run(self):
        while True:
            snapshot, attackers = self.analyze_packets()
            if self.check_alerts(snapshot, attackers):
                time.sleep(4)
            else:
                top_type, top_count = self.get_top_type()
                self.show_status(top_type, top_count)
                time.sleep(1)

if __name__ == "__main__":
    LWNIDS().run()
