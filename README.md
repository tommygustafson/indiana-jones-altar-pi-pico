# Indiana Jones - Fertility Idol Altar
This is the code that connects the PN532 RFID reader, activates the linear actuator and can also communicate with other devices with ESP322 radio

- Pi zero -> runs altar_pn532.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio
- Pi 3 -> runs listen-act.py, which receives the RFID key tag string via ESP322 and can then act based on this tag

Working on using Github Desktop

-------------------------------------

Wiring diagram and moduels used on Pi zero
- runs altar_pn532.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio

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

--------------------------------------

Tips for use of Git / Github:
- Git commit -am “commit notes”
- Git push origin main   # pushes changes on pi’s to GitHub
- Git pull origin main  # pulls or gets files from Github to pi

- BIG CHANGES!!!!!
