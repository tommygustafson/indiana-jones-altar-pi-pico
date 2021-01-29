import time
import struct
import board
import digitalio as dio
# if running this on a ATSAMD21 M0 based board
# from circuitpython_nrf24l01.rf24_lite import RF24
from circuitpython_nrf24l01.rf24 import RF24


# addresses needs to be in a buffer protocol object (bytearray)
address = b"1Node"

# change these (digital output) pins accordingly
ce = dio.DigitalInOut(board.D4)
csn = dio.DigitalInOut(board.D5)

# using board.SPI() automatically selects the MCU's
# available SPI pins, board.SCK, board.MOSI, board.MISO
spi = board.SPI()  # init spi bus object

# we'll be using the dynamic payload size feature (enabled by default)
# initialize the nRF24L01 on the spi bus object
nrf = RF24(spi, csn, ce)

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity
nrf.pa_level = -12

nrf.open_rx_pipe(0, address)
nrf.listen = True  # put radio into RX mode and power up

listen = True

start = time.monotonic()

print("Starting listening loop")

while listen:
    if nrf.update() and nrf.pipe is not None:
        # print details about the received packet
        print("{} bytes received on pipe {}".format(nrf.any(), nrf.pipe))
        # fetch 1 payload from RX FIFO
        rx = nrf.recv()  # also clears nrf.irq_dr status flag
        # expecting an int, thus the string format '<i'
        # the rx[:4] is just in case dynamic payloads were disabled
        
        #buffer = struct.unpack("<i", rx[:4])  # [:4] truncates padded 0s
        buffer = struct.unpack("<q",rx)
        #################
        # in struct.pack, "i" uses a 4 byte int
        # "q" uses an 8 byte int
        #################

        # print the only item in the resulting tuple from
        # using `struct.unpack()`
        print("Received: {}, Raw: {}".format(buffer[0], rx))
        start = time.monotonic()  
    time.sleep(0.25)
    print(".",end='')      

    # recommended behavior is to keep in TX mode while idle
nrf.listen = False  # put the nRF24L01 is in TX mode