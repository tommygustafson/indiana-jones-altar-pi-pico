"""
  Interface RFid RC522 Reader using Maker Pi Pico and CircuitPython
  
  Items:
  – Maker Pi Pico
    https://my.cytron.io/p-maker-pi-pico
  – Mifare RC522 RFID Kit
    https://my.cytron.io/p-mifare-rc522-rfid-kit
  – Grove – Relay
    https://my.cytron.io/p-grove-relay
  – USB Micro B Cable
    https://my.cytron.io/p-usb-micro-b-cable
  
  Libraries required from bundle (https://circuitpython.org/libraries):
  – simpleio.mpy
  - adafruit_bus_device (folder)
  
  Other libraries required:
  - mfrc522 (https://github.com/domdfcoding/circuitpython-mfrc522)
  - circuitpython_nrf24l01 (folder) (https://github.com/nRF24/CircuitPython_nRF24L01)
  
  References:
  – https://github.com/domdfcoding/circuitpython-mfrc522
  - https://tutorial.cytron.io/2022/01/11/interface-rfid-rc522-reader-using-maker-pi-pico-and-circuitpython/
   
For Git:
Git commit -am “commit notes”
Git push origin main --> pushes changes to GitHub
Git pull origin main --> pulls / gets / updates files from Github
   
"""

import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
import struct
from circuitpython_nrf24l01.rf24 import RF24
import simpleio
import mfrc522

'''
###############################
# Set up digital pins for control of relay
# input 1 = GP20
# input 2 = GP21
###############################

'''

relay_1 = DigitalInOut(board.GP21) #BLUE, IN1
relay_2 = DigitalInOut(board.GP20) #GREEN, IN2

relay_1.direction = Direction.OUTPUT
relay_2.direction = Direction.OUTPUT

'''
# For relay outputs, a value of FALSE is ON / ACTIVE on relay
# and value of TRUE is OFF / INACTIVE on relay
#
# To extend linear actuator: relay_1 = True, relay_2 = False
# To retract linear actuator: relay_1 = False, relay_2 = True
# To pause / stop: relay_1 = relay_2 = True
'''

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
'''
#######################################
# process_tag
# here, will perform actions / send nrf data based on tag
# Consider, taking no action if same tag present from cycle to cyle,
#   but will need to ensure we don't skip actions between long times of same tag
#
#######################################
'''

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
#####
# Set up LED pin
#####
'''
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

#pixel_pin = board.NEOPIXEL

#num_pixels = 1

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
#ORDER = neopixel.RGB

#pixels = neopixel.NeoPixel(
#    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
#)

#reset_pin = DigitalInOut(board.D6)


'''
############################################
# SPI connection:
############################################

Set up SPI connection for the RC522 RFID reader

cd = SDA = GP5


'''
sck = board.GP6
mosi = board.GP7
miso = board.GP4
spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

cs = DigitalInOut(board.GP5)
rst = DigitalInOut(board.GP8)
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

print("setup RC522 complete")

# Create string from hex code to compare items
tag_list = []
prior_tag_str = ""

'''
##################
# Set up nrf
##################

'''
'''
print("Setting up nRF")
# addresses needs to be in a buffer protocol object (bytearray)
address = b"1Node"
ce_nrf_pin = DigitalInOut(board.GP2)
csn_nrf_pin = DigitalInOut(board.GP3)
nrf = RF24(spi, csn_nrf_pin, ce_nrf_pin)

nrf.open_tx_pipe(address)  # set address of RX node into a TX pipe
nrf.listen = False  # ensures the nRF24L01 is in TX mode

print("#######")
print("Setup of nRF completed")
print("#######")
'''

print("Waiting for RFID/NFC card...")

prev_data = ""

while True:
    # Check if a card is available to read
    # uid = pn532.read_passive_target(timeout=0.5)
    
    (status, tag_type) = rfid.request(rfid.REQALL)
    print(status)
    print(tag_type)
    
    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()
        rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
        print("Card detected! UID: {}".format(rfid_data))
    
    '''
    if uid is None:
        prior_tag_str = ""
        if is_actuator_moving():
            stop_actuator()
        continue
    '''
    
    #prior_tag_str = process_tag(tag_list,uid,prior_tag_str)
    
    time.sleep(1)
