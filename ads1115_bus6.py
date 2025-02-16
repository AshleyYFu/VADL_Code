import time
import smbus

I2C_BUS = 6
DEVICE_ADDRESS = 0x48

# ADS1115 Registers
POINTER_CONVERSION = 0x00
POINTER_CONFIGURATION = 0x01

# Initialize I2C
bus = smbus.SMBus(I2C_BUS)

def swap2Bytes(c):
    """Swap byte order for 16-bit values."""
    return (c >> 8 | c << 8) & 0xFFFF

def LEtoBE(c):
    """Convert little-endian to big-endian."""
    c = swap2Bytes(c)
    if c >= 2**15:
        c = c - 2**16
    return c

def read_ads1115():
    """Reads a single value from channel 0 (AIN0)."""
    # Configuration: Single-shot mode, AIN0, 4.096V range, 128 SPS
    conf = swap2Bytes(0b1100000110000011)  
    bus.write_word_data(DEVICE_ADDRESS, POINTER_CONFIGURATION, conf)

    # Wait for conversion (at least 8ms for 128 SPS)
    time.sleep(0.01)

    # Read conversion result
    raw_value = bus.read_word_data(DEVICE_ADDRESS, POINTER_CONVERSION)
    value = LEtoBE(raw_value)

    return value

def calc_vbat(adc_val):
    r1 = 330000
    r2 = 100000
    vDivider = r2/(r2+r1)

    return adc_val/vDivider

try:
    while True:
        raw_adc_value = read_ads1115()
        real_adc_value = raw_adc_value * 0.1875 / 1000
        
        formatted_adc = "%.6f" % real_adc_value
        vbat = calc_vbat(real_adc_value)

        print(f"ADC Value: {formatted_adc} V    Battery Value: {vbat} V")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    bus.close()
