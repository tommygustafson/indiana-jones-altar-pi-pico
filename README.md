# Indiana Jones - Fertility Idol Altar
This is the code that connects the PN532 RFID reader, activates the linear actuator and can also communicate with other devices with RFM69 packet radio

Plan for all devices to run on Raspberry Pi Pico (RP2040) based boards with RFM69 packet radios, currently using:
Adafruit Feather RP2040 RFM69 Packet Radio (868 or 915 MHz)
- https://www.adafruit.com/product/5712

The project is designed to run under Micropython, NOT Circuitpython due to storage limitations
- In general, we will use Thonny to save files to the Pico and to edit code
- Guide: https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0

RFID reader:
- RC522
- - https://github.com/danjperron/micropython-mfrc522/tree/master
  - Plan to use the SPI interface
  - Another example: https://how2electronics.com/using-rc522-rfid-reader-module-with-raspberry-pi-pico/
  - Another example: https://microcontrollerslab.com/raspberry-pi-pico-rfid-rc522-micropython/#google_vignette

Basic arrangement
- Pi Pico #1 -> runs altar_rc522.py which drives the RC522 RFID reader, controls linear actuator and sends commands to other devices with RFM69 packet radio
- Pi Pico #2,... -> runs listen-act.py, which receives the RFID key tag string via RFM69 packet radio and can then act based on this tag

Working on using Github Desktop

-------------------------------------

Wiring diagram and moduels used on Pi zero
- runs altar_rc522.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio

Other libraries required:
  - adafruit_pn532.mpy
  - circuitpython_nrf24l01 (folder) (https://github.com/nRF24/CircuitPython_nRF24L01)

Example Code for PN532:
  - Example code from PN532 library page
    --> https://docs.circuitpython.org/projects/pn532/en/latest/examples.html
  - Example code for UART
    --> https://github.com/StevenSeagull1/raspbery_pico/tree/main
  - Example code for SPI
    --> https://stackoverflow.com/questions/73194125/select-apdu-command-on-raspberry-pi-pico-with-pn532-repond-nothing
  
  References:
  - https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
    --> Info specifically on SPI bus
  - https://learn.adafruit.com/adafruit-pn532-rfid-nfc/python-circuitpython
    -->  Installing the PN532 libraries, wiring diagrams for the PN532 breakout board
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
    --> Installing the nrf libraries, wiring, pinouts for the NRF42l01 wireless transceiver

--------------------------------------

Tips for use of Git / Github:
- Git commit -am “commit notes”
- Git push origin main   # pushes changes on pi’s to GitHub
- Git pull origin main  # pulls or gets files from Github to pi

- BIG CHANGES!!!!!
