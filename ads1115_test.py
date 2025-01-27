#https://www.youtube.com/watch?v=fBUElwY3yrs
#https://www.instructables.com/How-to-Use-ADS1115-With-the-Raspberry-Pi-Part-1/

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS object and specify the gain
ads = ADS.ADS1115(i2c)

# Can change based on the voltage signal - Gain of 1 is typically enough but double check this
ads.gain = 1
chan = AnalogIn(ads, ADS.P0)

# Continuously print the values
while True:
    print(f"voltage read: {chan.voltage}V")
    time.sleep(0.5)