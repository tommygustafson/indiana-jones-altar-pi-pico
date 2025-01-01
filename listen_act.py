import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
import adafruit_rfm69
from adafruit_datetime import datetime

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

### Define Chip Select and Reset pins for the radio module.
#CS = digitalio.DigitalInOut(board.RFM_CS)
#RESET = digitalio.DigitalInOut(board.RFM_RST)

### Initialise RFM69 radio
#rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

### Wait to receive packets.
print("Waiting for packets...")
while True:
    # Look for a new packet - wait up to 5 seconds:
    packet = rfm69.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        print("Received a packet!")
        # If the received packet is b'button'...
        packet_str = packet.decode("utf-8")
        print(packet_str)
        if packet_str == "false-idol":
            # ...cycle the NeoPixel LED color through the color_values list.
            print("FALSE IDOL")