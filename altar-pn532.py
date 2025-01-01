"""
  Interface RFid PN-532 Reader using CircuitPython on Raspberry Pi Pico
  
  https://github.com/adafruit/Adafruit_CircuitPython_PN532
  
  Example code of someone using with Pi Pico:
  https://stackoverflow.com/questions/73194125/select-apdu-command-on-raspberry-pi-pico-with-pn532-repond-nothing
  
  Other libraries required:
  - adafruit_pn532
  - circuitpython_nrf24l01 (folder) (https://github.com/nRF24/CircuitPython_nRF24L01)
  
  References:
  – https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
    --> Installs circuit python libraries, checks a bunch of useful config items (SSH, SPI)
  - https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
    --> Info specifically on SPI bus
  - https://learn.adafruit.com/adafruit-pn532-rfid-nfc/python-circuitpython
    -->  Installing the PN532 libraries, wiring diagrams for the PN532 breakout board
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
    --> Installing the nrf libraries, wiring, pinouts for the NRF42l01 wireless transceiver
   
For Git:  Use PowerShell
Git commit -am “commit notes”
Git push origin main --> pushes changes to GitHub
Git pull origin main --> pulls / gets / updates files from Github
   
"""
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
from adafruit_pn532.spi import PN532_SPI
import adafruit_rfm69
from adafruit_datetime import datetime

'''
###############################
# Set up digital pins for control of relay
# input 1 = D.20
# input 2 = D.21

Also need to attach on relay, vcc to 5v on Rpi and gnd to ground on Rpi

###############################

'''

relay_1 = DigitalInOut(board.GP27) #BLUE, IN1
relay_2 = DigitalInOut(board.GP26) #GREEN, IN2

relay_1.direction = Direction.OUTPUT
relay_2.direction = Direction.OUTPUT

'''
#########################
# For relay outputs, a value of FALSE is ON / ACTIVE on relay
# and value of TRUE is OFF / INACTIVE on relay
#
# To extend linear actuator: relay_1 = True, relay_2 = False
# To retract linear actuator: relay_1 = False, relay_2 = True
# To pause / stop: relay_1 = True, relay_2 = True
##########################
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
    # TO DO: Make extend and retractor tag as lists to allow multiple tags / objects
    extend_actuator_tag = "56146162137"
    retract_actuator_tag = "24023514149"

    print(datetime.now())

    tag_str = add_tag_to_list(tag_list,uid)
    print("Processing tag: ", tag_str)
    #print(tag_list)

    if prior_tag_str == tag_str:
        print("Same tag on sensor, take no action")
        #stop_actuator()
    else:
        print("New tag detected, taking action and send data")
        #send_data_nrf(tag_str)
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

def send_data_rfm69(str_to_send):
    rfm69.send(bytes(str_to_send, "UTF-8"))
    
'''
#####
# Set up LED pin
#####
'''
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT


'''
############################################
# SPI connection:
############################################
Set up SPI connection for the PN532 RFID reader
'''

print("Starting setup of PN532")
SCK = board.GP18
MISO = board.GP16
MOSI = board.GP19
spi = busio.SPI(SCK, MOSI, MISO)
cs_pin = DigitalInOut(board.GP17)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Create string from hex code to compare items
tag_list = []
prior_tag_str = ""

print("#######")
print("Setup of PN532 completed")
print("#######")

'''
##################
# Set up RFM69 packet radio
##################
'''
print("Setting up RFM69 packet radio")

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

'''
# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

str_to_send = "button"
send_data_rfm69(str_to_send)
'''

print("#######")
print("Setup of RFM69 packet radio completed")
print("#######")

print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    # Try again if no card is available.
    if uid is None:
        prior_tag_str = ""
        if is_actuator_moving():
            stop_actuator()
        continue
    #print("Found card with UID:", [hex(i) for i in uid])
    #print("Found card with UID in str:", [str(i) for i in uid])
    prior_tag_str = process_tag(tag_list,uid,prior_tag_str)    
    time.sleep(0.5)

