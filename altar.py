'''
Code example
https://circuitpython.readthedocs.io/projects/pn532/en/latest/examples.html
'''

import board
import busio
#from digitalio import DigitalInOut
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pn532.spi import PN532_SPI
import digitalio
import time
import struct
#import neopixel
from circuitpython_nrf24l01.rf24 import RF24


###############################
# Set up digital pins for control of relay
# input 1 = D.20
# input 2 = D.21
###############################
relay_1 = DigitalInOut(board.D21) #BLUE, IN1
relay_2 = DigitalInOut(board.D20) #GREEN, IN2

relay_1.direction = Direction.OUTPUT
relay_2.direction = Direction.OUTPUT

# For relay outputs, a value of FALSE is ON / ACTIVE on relay
# and value of TRUE is OFF / INACTIVE on relay
#
# To extend linear actuator: relay_1 = True, relay_2 = False
# To retract linear actuator: relay_1 = False, relay_2 = True
# To pause / stop: relay_1 = relay_2 = True
relay_1.value = True
relay_2.value = True

#def add_tag_to_list(tag_list, uid, pixels):
def add_tag_to_list(tag_list, uid):
    tag_str = ''
    tag_int = 0
    for i in uid:
        tag_str += str(i)
        tag_int += int(i)
    if tag_str not in tag_list:
        tag_list.append(tag_str)
        print("added tag ",tag_str," to tag list")
        #pixels.fill(GREEN)
    else:
        throw_away = 1
        #print("Tag ", tag_str, " already in list")
        #print("Sending tag_int = ", tag_int)
        #send_data_nrf(tag_int)
        #send_data_nrf(tag_str)
    return tag_str

#######################################
# process_tag
# here, will perform actions / send nrf data based on tag
# Consider, taking no action if same tag present from cycle to cyle,
#   but will need to ensure we don't skip actions between long times of same tag
#
#######################################
def process_tag(tag_list,uid,prior_tag_str):
    extend_actuator_tag = "25224315051"
    retract_actuator_tag = "141219112"

    tag_str = add_tag_to_list(tag_list,uid)
    print("Processing tag: ", tag_str)

    if prior_tag_str == tag_str:
        print("Same tag on sensor, take no action")
        #stop_actuator()
    else:
        print("New tag detected, taking action and send data")
        send_data_nrf(tag_str)
        if tag_str == extend_actuator_tag:
            extend_actuator()
        if tag_str == retract_actuator_tag:
            retract_actuator()


    # Return current tag_str to become prior_tag_str
    print("---------")
    return tag_str

def extend_actuator():
    print("Extending actuator")
    relay_1.value = False
    relay_2.value = True

def retract_actuator():
    print("Retracting actuator")
    relay_1.value = True
    relay_2.value = False

def stop_actuator():
    print("Stop actuator")
    relay_1.value = True
    relay_2.value = True

def is_actuator_moving():
    if relay_1.value == False or relay_2.value == False:
        return True
    else:
        return False

def send_data_nrf(data):
    #data = 1234
    #buffer = struct.pack("<i", int(data))
    buffer = struct.pack("<q", int(data))
    #################
    # in struct.pack, "i" uses a 4 byte int
    # "q" uses an 8 byte int
    #################

    print("Sending: {} as struct: {}".format(data, buffer))
    start_timer = time.monotonic() * 1000  # start timer
    result = nrf.send(buffer)
    end_timer = time.monotonic() * 1000  # end timer
    if not result:
        print("send() failed or timed out")
    else:
        print("send() successful")
        # print timer results despite transmission success
        print("Transmission took", end_timer - start_timer, "ms")


'''
Set up Neopixel
'''
#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT

#pixel_pin = board.NEOPIXEL

#num_pixels = 1

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
#ORDER = neopixel.RGB

#pixels = neopixel.NeoPixel(
#    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
#)

#reset_pin = DigitalInOut(board.D6)



############################################
# SPI connection:
############################################
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

print("setup PN532 complete")
ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Create string from hex code to compare items
tag_list = []
prior_tag_str = ""

##################
# Set up nrf
##################
print("Setting up nRF")
# addresses needs to be in a buffer protocol object (bytearray)
address = b"1Node"
ce_nrf_pin = DigitalInOut(board.D2)
csn_nrf_pin = DigitalInOut(board.D3)
nrf = RF24(spi, csn_nrf_pin, ce_nrf_pin)

nrf.open_tx_pipe(address)  # set address of RX node into a TX pipe
nrf.listen = False  # ensures the nRF24L01 is in TX mode

print("#######")
print("Setup of PN532 and nRF completed")
print("#######")

print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    #pixels.fill(YELLOW)
    #pixels.show()
    #print(".", end="")
    # Try again if no card is available.
    if uid is None:
        prior_tag_str = ""
        if is_actuator_moving():
            stop_actuator()
        continue
    #print("Found card with UID:", [hex(i) for i in uid])
    #print("Found card with UID in str:", [str(i) for i in uid])
    prior_tag_str = process_tag(tag_list,uid,prior_tag_str)    
    time.sleep(0.25)